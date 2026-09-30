from fastapi import APIRouter, HTTPException
import httpx
import re

from github_service import (
    get_repository,
    get_file_content,
    get_repository_tree,
    create_branch,
    update_file,
    commit_multiple_files,
    create_pull_request,
)
from test_service import run_branch_tests
from schemas.github import (
    UpdateFileRequest,
    ApplyCodeChangesRequest,
    CreateFeatureBranchRequest,
    CreatePullRequestRequest,
)

router = APIRouter(prefix="/github", tags=["GitHub"])

def generate_branch_name(issue_key: str, summary: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", summary.lower()).strip("-")
    slug = slug[:50].rstrip("-")
    return f"feature/{issue_key.lower()}-{slug}"

@router.get("/repository")
async def github_repository():
    try:
        repository = await get_repository()
        return {
            "name": repository["name"],
            "full_name": repository["full_name"],
            "private": repository["private"],
            "default_branch": repository["default_branch"],
            "html_url": repository["html_url"],
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/file")
async def github_file(path: str):
    try:
        return await get_file_content(path)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/tree")
async def github_tree():
    try:
        tree = await get_repository_tree()
        files = [item["path"] for item in tree["tree"] if item["type"] == "blob"]
        repository = await get_repository()
        return {"repository": repository["name"], "branch": repository["default_branch"], "files": files}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/branch")
async def github_branch(branch_name: str, base_branch: str = "main"):
    try:
        return await create_branch(branch_name, base_branch)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/file")
async def github_update_file(request: UpdateFileRequest):
    try:
        return await update_file(
            file_path=request.path,
            content=request.content,
            branch=request.branch,
            commit_message=request.message,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/feature-branch")
async def github_feature_branch(request: CreateFeatureBranchRequest):
    try:
        branch_name = generate_branch_name(request.issue_key, request.summary)
        result = await create_branch(branch_name=branch_name, base_branch="main")
        return {
            "issue_key": request.issue_key,
            "branch": branch_name,
            "base_branch": "main",
            "sha": result.get("sha"),
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/apply-changes")
async def github_apply_changes(request: ApplyCodeChangesRequest):
    try:
        if not request.branch:
            raise HTTPException(status_code=400, detail="Branch is required.")
        if not request.changes:
            raise HTTPException(status_code=400, detail="No code changes provided.")

        result = await commit_multiple_files(
            branch=request.branch,
            changes=[change.model_dump() for change in request.changes],
            commit_message=f"{request.issue_key}: Implement requested changes",
        )
        return {
            "success": True,
            "issue_key": request.issue_key,
            "branch": result["branch"],
            "commit_sha": result["commit_sha"],
            "commit_url": result["commit_url"],
            "files_changed": result["files_changed"],
        }
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=e.response.status_code, detail=e.response.text)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/test")
async def test_github_branch(branch: str):
    try:
        return {"branch": branch, **await run_branch_tests(branch)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/pull-request")
async def github_pull_request(request: CreatePullRequestRequest):
    try:
        title = f"{request.issue_key}: {request.summary}"
        body = f"""## Jira Ticket

{request.issue_key}

## Description

{request.description}

## Commit

{request.commit_sha}
"""
        result = await create_pull_request(
            title=title,
            body=body,
            head=request.branch,
            base="main",
        )
        return {"success": True, "issue_key": request.issue_key, "pull_request": result}
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=e.response.status_code, detail=e.response.text)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
