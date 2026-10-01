import re

from services.github_service import (
    create_branch,
    commit_multiple_files,
    create_pull_request,
)
from services.test_service import run_branch_tests


def generate_branch_name(issue_key: str, summary: str) -> str:
    slug = summary.lower()
    slug = re.sub(r"[^a-z0-9]+", "-", slug)
    slug = slug.strip("-")
    slug = slug[:50].rstrip("-")
    return f"feature/{issue_key.lower()}-{slug}"


async def create_feature_branch(issue_key: str, summary: str):
    branch_name = generate_branch_name(issue_key, summary)
    result = await create_branch(
        branch_name=branch_name,
        base_branch="main",
    )
    return {
        "issue_key": issue_key,
        "branch": branch_name,
        "base_branch": "main",
        "sha": result.get("sha"),
    }


async def apply_code_changes(branch: str, issue_key: str, changes: list[dict]):
    if not branch:
        raise ValueError("Branch is required.")
    if not changes:
        raise ValueError("No code changes provided.")

    result = await commit_multiple_files(
        branch=branch,
        changes=changes,
        commit_message=f"{issue_key}: Implement requested changes",
    )
    return {
        "success": True,
        "issue_key": issue_key,
        "branch": result["branch"],
        "commit_sha": result["commit_sha"],
        "commit_url": result["commit_url"],
        "files_changed": result["files_changed"],
    }


async def test_branch(branch: str):
    return await run_branch_tests(branch)


async def create_github_pull_request(
    issue_key: str,
    summary: str,
    description: str,
    branch: str,
    commit_sha: str,
):
    title = f"{issue_key}: {summary}"
    body = f"""
## Jira Ticket

{issue_key}

## Description

{description}

## Commit

{commit_sha}
"""
    result = await create_pull_request(
        title=title,
        body=body,
        head=branch,
        base="main",
    )
    return {
        "success": True,
        "issue_key": issue_key,
        "pull_request": result,
    }
