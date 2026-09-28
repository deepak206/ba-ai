import os
import httpx
from dotenv import load_dotenv


load_dotenv()


# ============================================================
# GitHub Configuration
# ============================================================

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
GITHUB_OWNER = os.getenv("GITHUB_OWNER")
GITHUB_REPO = os.getenv("GITHUB_REPO")

GITHUB_API_URL = "https://api.github.com"


GITHUB_HEADERS = {
    "Accept": "application/vnd.github+json",
    "Authorization": f"Bearer {GITHUB_TOKEN}",
    "X-GitHub-Api-Version": "2022-11-28",
}


# ============================================================
# Repository
# ============================================================

async def get_repository():
    url = (
        f"{GITHUB_API_URL}/repos/"
        f"{GITHUB_OWNER}/{GITHUB_REPO}"
    )

    async with httpx.AsyncClient() as client:

        response = await client.get(
            url,
            headers=GITHUB_HEADERS,
        )

        response.raise_for_status()

        return response.json()


# ============================================================
# Repository Tree
# ============================================================

async def get_repository_tree(
    branch: str = "main",
):
    print(
        ">>> Getting GitHub repository tree..."
    )

    url = (
        f"{GITHUB_API_URL}/repos/"
        f"{GITHUB_OWNER}/{GITHUB_REPO}"
        f"/git/trees/{branch}?recursive=1"
    )

    async with httpx.AsyncClient() as client:

        response = await client.get(
            url,
            headers=GITHUB_HEADERS,
        )

        print(
            ">>> GitHub tree status:",
            response.status_code,
        )

        response.raise_for_status()

        data = response.json()

    files = [
        item["path"]
        for item in data.get("tree", [])
        if item.get("type") == "blob"
    ]

    print(
        ">>> Repository files:",
        len(files),
    )

    for file in files:
        print(
            "   ",
            file,
        )

    return {
        "repository": (
            f"{GITHUB_OWNER}/{GITHUB_REPO}"
        ),
        "branch": branch,
        "files": files,
    }


# ============================================================
# Get File Content
# ============================================================

async def get_file_content(
    file_path: str,
    branch: str = "main",
):
    print(
        f">>> Getting file: {file_path}"
    )

    url = (
        f"{GITHUB_API_URL}/repos/"
        f"{GITHUB_OWNER}/{GITHUB_REPO}"
        f"/contents/{file_path}"
    )

    params = {
        "ref": branch,
    }

    async with httpx.AsyncClient() as client:

        response = await client.get(
            url,
            headers=GITHUB_HEADERS,
            params=params,
        )

        response.raise_for_status()

        data = response.json()

    # GitHub returns base64 encoded content
    import base64

    encoded_content = data.get(
        "content",
        "",
    )

    content = base64.b64decode(
        encoded_content
    ).decode(
        "utf-8"
    )

    return {
        "path": file_path,
        "content": content,
        "sha": data.get("sha"),
    }


# ============================================================
# Create Branch
# ============================================================

async def create_branch(
    branch_name: str,
    base_branch: str = "main",
):
    print(
        f">>> Creating branch: {branch_name}"
    )

    # --------------------------------------------------------
    # Get base branch
    # --------------------------------------------------------

    url = (
        f"{GITHUB_API_URL}/repos/"
        f"{GITHUB_OWNER}/{GITHUB_REPO}"
        f"/git/ref/heads/{base_branch}"
    )

    async with httpx.AsyncClient() as client:

        response = await client.get(
            url,
            headers=GITHUB_HEADERS,
        )

        response.raise_for_status()

        base_ref = response.json()

    base_sha = base_ref[
        "object"
    ][
        "sha"
    ]

    # --------------------------------------------------------
    # Create new branch
    # --------------------------------------------------------

    create_url = (
        f"{GITHUB_API_URL}/repos/"
        f"{GITHUB_OWNER}/{GITHUB_REPO}"
        f"/git/refs"
    )

    payload = {
        "ref": f"refs/heads/{branch_name}",
        "sha": base_sha,
    }

    async with httpx.AsyncClient() as client:

        response = await client.post(
            create_url,
            headers=GITHUB_HEADERS,
            json=payload,
        )

        response.raise_for_status()

        result = response.json()

    print(
        ">>> Branch created:",
        branch_name,
    )

    return {
        "branch": branch_name,
        "sha": base_sha,
        "ref": result.get("ref"),
    }


# ============================================================
# Get Branch Reference
# ============================================================

async def get_branch_reference(
    branch: str,
):
    url = (
        f"{GITHUB_API_URL}/repos/"
        f"{GITHUB_OWNER}/{GITHUB_REPO}"
        f"/git/ref/heads/{branch}"
    )

    async with httpx.AsyncClient() as client:

        response = await client.get(
            url,
            headers=GITHUB_HEADERS,
        )

        response.raise_for_status()

        return response.json()


# ============================================================
# Get Commit
# ============================================================

async def get_commit(
    commit_sha: str,
):
    url = (
        f"{GITHUB_API_URL}/repos/"
        f"{GITHUB_OWNER}/{GITHUB_REPO}"
        f"/git/commits/{commit_sha}"
    )

    async with httpx.AsyncClient() as client:

        response = await client.get(
            url,
            headers=GITHUB_HEADERS,
        )

        response.raise_for_status()

        return response.json()


# ============================================================
# Create Git Blob
# ============================================================

async def create_git_blob(
    content: str,
):
    url = (
        f"{GITHUB_API_URL}/repos/"
        f"{GITHUB_OWNER}/{GITHUB_REPO}"
        f"/git/blobs"
    )

    payload = {
        "content": content,
        "encoding": "utf-8",
    }

    async with httpx.AsyncClient() as client:

        response = await client.post(
            url,
            headers=GITHUB_HEADERS,
            json=payload,
        )

        response.raise_for_status()

        return response.json()


# ============================================================
# Create Git Tree
# ============================================================

async def create_git_tree(
    base_tree_sha: str,
    tree_entries: list[dict],
):
    url = (
        f"{GITHUB_API_URL}/repos/"
        f"{GITHUB_OWNER}/{GITHUB_REPO}"
        f"/git/trees"
    )

    payload = {
        "base_tree": base_tree_sha,
        "tree": tree_entries,
    }

    async with httpx.AsyncClient() as client:

        response = await client.post(
            url,
            headers=GITHUB_HEADERS,
            json=payload,
        )

        response.raise_for_status()

        return response.json()


# ============================================================
# Create Git Commit
# ============================================================

async def create_git_commit(
    message: str,
    tree_sha: str,
    parent_sha: str,
):
    url = (
        f"{GITHUB_API_URL}/repos/"
        f"{GITHUB_OWNER}/{GITHUB_REPO}"
        f"/git/commits"
    )

    payload = {
        "message": message,
        "tree": tree_sha,
        "parents": [
            parent_sha,
        ],
    }

    async with httpx.AsyncClient() as client:

        response = await client.post(
            url,
            headers=GITHUB_HEADERS,
            json=payload,
        )

        response.raise_for_status()

        return response.json()


# ============================================================
# Update Branch Reference
# ============================================================

async def update_branch_reference(
    branch: str,
    commit_sha: str,
):
    url = (
        f"{GITHUB_API_URL}/repos/"
        f"{GITHUB_OWNER}/{GITHUB_REPO}"
        f"/git/refs/heads/{branch}"
    )

    payload = {
        "sha": commit_sha,
        "force": False,
    }

    async with httpx.AsyncClient() as client:

        response = await client.patch(
            url,
            headers=GITHUB_HEADERS,
            json=payload,
        )

        response.raise_for_status()

        return response.json()


# ============================================================
# Commit Multiple Files
#
# Supports:
#
# CREATE
# MODIFY
#
# All changes are included in ONE commit.
# ============================================================

async def commit_multiple_files(
    branch: str,
    changes: list[dict],
    commit_message: str,
):

    if not changes:

        raise ValueError(
            "No approved code changes were provided."
        )

    print(
        ">>> COMMIT MULTIPLE FILES"
    )

    print(
        ">>> Branch:",
        branch,
    )

    print(
        ">>> Number of changes:",
        len(changes),
    )

    # --------------------------------------------------------
    # Get current branch
    # --------------------------------------------------------

    branch_ref = await get_branch_reference(
        branch
    )

    parent_sha = branch_ref[
        "object"
    ][
        "sha"
    ]

    print(
        ">>> Parent commit:",
        parent_sha,
    )

    # --------------------------------------------------------
    # Get parent commit
    # --------------------------------------------------------

    parent_commit = await get_commit(
        parent_sha
    )

    base_tree_sha = parent_commit[
        "tree"
    ][
        "sha"
    ]

    print(
        ">>> Base tree:",
        base_tree_sha,
    )

    # --------------------------------------------------------
    # Build tree entries
    # --------------------------------------------------------

    tree_entries = []

    for change in changes:

        file_path = change.get(
            "file"
        )

        new_content = change.get(
            "new_content"
        )

        action = change.get(
            "action",
            "modify",
        )

        # ----------------------------------------------------
        # Validate file path
        # ----------------------------------------------------

        if not file_path:

            raise ValueError(
                "Every code change must contain a file path."
            )

        # ----------------------------------------------------
        # Validate action
        # ----------------------------------------------------

        if action not in [
            "create",
            "modify",
        ]:

            raise ValueError(
                f"Unsupported action for "
                f"{file_path}: {action}"
            )

        # ----------------------------------------------------
        # Validate content
        # ----------------------------------------------------

        if new_content is None:

            raise ValueError(
                f"No new_content provided for "
                f"{file_path}"
            )

        # ----------------------------------------------------
        # Security validation
        # ----------------------------------------------------

        normalized_path = file_path.replace(
            "\\",
            "/",
        )

        if normalized_path.startswith(
            "/"
        ):

            raise ValueError(
                f"Absolute paths are not allowed: "
                f"{file_path}"
            )

        if normalized_path.startswith(
            "../"
        ):

            raise ValueError(
                f"Parent directory paths are not allowed: "
                f"{file_path}"
            )

        if "/../" in normalized_path:

            raise ValueError(
                f"Parent directory paths are not allowed: "
                f"{file_path}"
            )

        if normalized_path == ".git":

            raise ValueError(
                "Modifying .git is not allowed."
            )

        if normalized_path.startswith(
            ".git/"
        ):

            raise ValueError(
                "Modifying .git files is not allowed."
            )

        print(
            f">>> {action.upper()}: "
            f"{normalized_path}"
        )

        # ----------------------------------------------------
        # Create blob
        # ----------------------------------------------------

        blob = await create_git_blob(
            new_content
        )

        blob_sha = blob[
            "sha"
        ]

        print(
            ">>> Blob:",
            blob_sha,
        )

        # ----------------------------------------------------
        # Add tree entry
        #
        # CREATE:
        # New path is added.
        #
        # MODIFY:
        # Existing path is replaced.
        # ----------------------------------------------------

        tree_entries.append({
            "path": normalized_path,
            "mode": "100644",
            "type": "blob",
            "sha": blob_sha,
        })

    # --------------------------------------------------------
    # Create tree
    # --------------------------------------------------------

    new_tree = await create_git_tree(
        base_tree_sha=base_tree_sha,
        tree_entries=tree_entries,
    )

    new_tree_sha = new_tree[
        "sha"
    ]

    print(
        ">>> New tree:",
        new_tree_sha,
    )

    # --------------------------------------------------------
    # Create ONE commit
    # --------------------------------------------------------

    commit = await create_git_commit(
        message=commit_message,
        tree_sha=new_tree_sha,
        parent_sha=parent_sha,
    )

    commit_sha = commit[
        "sha"
    ]

    print(
        ">>> Commit created:",
        commit_sha,
    )

    # --------------------------------------------------------
    # Update branch
    # --------------------------------------------------------

    await update_branch_reference(
        branch=branch,
        commit_sha=commit_sha,
    )

    print(
        ">>> Branch updated:",
        branch,
    )

    return {
        "branch": branch,
        "commit_sha": commit_sha,
        "commit_url": commit[
            "html_url"
        ],
        "files_changed": [
            change["file"]
            for change in changes
        ],
    }


# ============================================================
# Create Pull Request
# ============================================================

async def create_pull_request(
    title: str,
    body: str,
    head: str,
    base: str = "main",
):

    url = (
        f"{GITHUB_API_URL}/repos/"
        f"{GITHUB_OWNER}/{GITHUB_REPO}"
        f"/pulls"
    )

    payload = {
        "title": title,
        "body": body,
        "head": head,
        "base": base,
    }

    async with httpx.AsyncClient() as client:

        response = await client.post(
            url,
            headers=GITHUB_HEADERS,
            json=payload,
        )

        response.raise_for_status()

        return response.json()
    
async def update_file(
    file_path: str,
    content: str,
    branch: str,
    commit_message: str,
):
    """
    Create or update a single file on GitHub.

    Kept for compatibility with existing API endpoints.
    For multiple AI-generated changes, prefer
    commit_multiple_files().
    """

    print(
        f">>> Updating file: {file_path}"
    )

    # --------------------------------------------------------
    # Get existing file
    # --------------------------------------------------------

    existing_sha = None

    try:

        existing_file = await get_file_content(
            file_path=file_path,
            branch=branch,
        )

        existing_sha = existing_file.get(
            "sha"
        )

    except httpx.HTTPStatusError as e:

        # 404 means the file does not exist.
        # That's okay — GitHub will create it.
        if e.response.status_code != 404:
            raise

        print(
            f">>> File does not exist. "
            f"Creating: {file_path}"
        )

    # --------------------------------------------------------
    # GitHub Contents API
    # --------------------------------------------------------

    import base64

    encoded_content = base64.b64encode(
        content.encode("utf-8")
    ).decode("utf-8")

    url = (
        f"{GITHUB_API_URL}/repos/"
        f"{GITHUB_OWNER}/{GITHUB_REPO}"
        f"/contents/{file_path}"
    )

    payload = {
        "message": commit_message,
        "content": encoded_content,
        "branch": branch,
    }

    # Existing file requires SHA
    if existing_sha:
        payload["sha"] = existing_sha

    async with httpx.AsyncClient() as client:

        response = await client.put(
            url,
            headers=GITHUB_HEADERS,
            json=payload,
        )

        response.raise_for_status()

        result = response.json()

    print(
        ">>> File updated successfully:",
        file_path,
    )

    return {
        "file": file_path,
        "branch": branch,
        "commit_sha": result.get(
            "commit",
            {}
        ).get(
            "sha"
        ),
        "content": result.get(
            "content"
        ),
    }