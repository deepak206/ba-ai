import os
import httpx
from dotenv import load_dotenv
import base64

load_dotenv()

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
GITHUB_OWNER = os.getenv("GITHUB_OWNER")
GITHUB_REPO = os.getenv("GITHUB_REPO")


async def get_repository():

    url = (
        f"https://api.github.com/repos/"
        f"{GITHUB_OWNER}/{GITHUB_REPO}"
    )

    headers = {
        "Accept": "application/vnd.github+json",
        "Authorization": f"Bearer {GITHUB_TOKEN}",
        "X-GitHub-Api-Version": "2022-11-28",
    }

    async with httpx.AsyncClient() as client:

        response = await client.get(
            url,
            headers=headers
        )

        response.raise_for_status()

        return response.json()
    
async def get_file_content(file_path: str):

    url = (
        f"https://api.github.com/repos/"
        f"{GITHUB_OWNER}/{GITHUB_REPO}/contents/{file_path}"
    )

    headers = {
        "Accept": "application/vnd.github+json",
        "Authorization": f"Bearer {GITHUB_TOKEN}",
        "X-GitHub-Api-Version": "2022-11-28",
    }

    async with httpx.AsyncClient() as client:

        response = await client.get(
            url,
            headers=headers
        )

        response.raise_for_status()

        data = response.json()

        content = base64.b64decode(
            data["content"]
        ).decode("utf-8")

        return {
            "path": data["path"],
            "content": content
        }
  
async def get_repository_tree():

    # First get the repository information
    repository = await get_repository()

    default_branch = repository["default_branch"]

    # Get branch information
    branch_url = (
        f"https://api.github.com/repos/"
        f"{GITHUB_OWNER}/{GITHUB_REPO}/branches/{default_branch}"
    )

    headers = {
        "Accept": "application/vnd.github+json",
        "Authorization": f"Bearer {GITHUB_TOKEN}",
        "X-GitHub-Api-Version": "2022-11-28",
    }

    async with httpx.AsyncClient() as client:

        branch_response = await client.get(
            branch_url,
            headers=headers
        )

        branch_response.raise_for_status()

        branch_data = branch_response.json()

        sha = branch_data["commit"]["sha"]

        # Get complete tree
        tree_url = (
            f"https://api.github.com/repos/"
            f"{GITHUB_OWNER}/{GITHUB_REPO}/git/trees/{sha}"
            f"?recursive=1"
        )

        tree_response = await client.get(
            tree_url,
            headers=headers
        )

        tree_response.raise_for_status()

        return tree_response.json()