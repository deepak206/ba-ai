import os
import shutil
import subprocess
import tempfile

from github_service import GITHUB_OWNER, GITHUB_REPO


async def run_branch_tests(branch: str):
    temp_dir = tempfile.mkdtemp(prefix="ai-agent-test-")

    try:
        repo_url = (
            f"https://github.com/"
            f"{GITHUB_OWNER}/{GITHUB_REPO}.git"
        )

        clone_url = (
            f"https://x-access-token:{os.getenv('GITHUB_TOKEN')}"
            f"@github.com/{GITHUB_OWNER}/{GITHUB_REPO}.git"
        )

        clone_result = subprocess.run(
            [
                "git",
                "clone",
                "--branch",
                branch,
                "--single-branch",
                clone_url,
                temp_dir,
            ],
            capture_output=True,
            text=True,
            timeout=120,
        )

        if clone_result.returncode != 0:
            return {
                "status": "failed",
                "stage": "clone",
                "output": clone_result.stderr,
            }

        test_command = detect_test_command(temp_dir)

        if not test_command:
            return {
                "status": "skipped",
                "stage": "test",
                "output": "No supported test command found.",
            }

        result = subprocess.run(
            test_command,
            cwd=temp_dir,
            capture_output=True,
            text=True,
            timeout=300,
            shell=True,
        )

        return {
            "status": "passed"
            if result.returncode == 0
            else "failed",
            "stage": "test",
            "command": test_command,
            "exit_code": result.returncode,
            "output": result.stdout,
            "error": result.stderr,
        }

    except subprocess.TimeoutExpired:
        return {
            "status": "failed",
            "stage": "test",
            "output": "Test execution timed out.",
        }

    except Exception as e:
        return {
            "status": "failed",
            "stage": "test",
            "output": str(e),
        }

    finally:
        shutil.rmtree(
            temp_dir,
            ignore_errors=True,
        )


def detect_test_command(project_path: str):
    package_json = os.path.join(
        project_path,
        "package.json",
    )

    if os.path.exists(package_json):
        return "npm test -- --run"

    requirements = os.path.join(
        project_path,
        "requirements.txt",
    )

    if os.path.exists(requirements):
        return "pytest"

    return None