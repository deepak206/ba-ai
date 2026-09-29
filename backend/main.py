from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import re
import httpx

from jira_service import (
    get_jira_issue,
    create_jira_issue,
    extract_adf_text,
    get_jira_transitions,
    move_jira_issue_to_in_progress,
    move_jira_issue_to_code_review,
)
from github_service import (
    get_repository,
    get_file_content,
    get_repository_tree,
    create_branch,
    update_file,
    commit_multiple_files,
    create_pull_request
)
from test_service import run_branch_tests
from pydantic import BaseModel
from ai.nodes import structure_requirement

from ai.graph import create_agent_graph
agent_graph = create_agent_graph()


class CreatePullRequestRequest(BaseModel):
    issue_key: str
    summary: str
    description: str
    branch: str
    commit_sha: str
    
class ApplyCodeChangesRequest(BaseModel):
    branch: str
    issue_key: str
    changes: list[dict]
    
class CodeChange(BaseModel):
    file: str
    action: str
    reason: str = ""
    changes: list[str] = []
    new_content: str


class ApplyCodeChangesRequest(BaseModel):
    branch: str
    issue_key: str
    changes: list[CodeChange]
    
class AnalyzeCodeRequest(BaseModel):
    issue_key: str
    summary: str
    description: str
    acceptance_criteria: list[str] = []
    technical_notes: list[str] = []
    test_requirements: list[str] = []
    repository_files: list[str]
    
class CreateFeatureBranchRequest(BaseModel):
    issue_key: str
    summary: str

class CreateJiraRequest(BaseModel):
    requirement: str
    
class FileChange(BaseModel):
    path: str
    content: str
    message: str


class ApplyChangesRequest(BaseModel):
    branch: str
    changes: list[FileChange]

class UpdateFileRequest(BaseModel):
    path: str
    content: str
    branch: str
    message: str
    
class AIAnalysisRequest(BaseModel):
    issue_key: str
    summary: str
    description: str
    
app = FastAPI(
    title="AI Development Agent",
    version="1.0.0"
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return {
        "message": "AI Development Agent API is running"
    }


@app.get("/jira/{issue_key}")
async def get_jira(issue_key: str):

    try:

        issue = await get_jira_issue(issue_key)

        description = extract_adf_text(
            issue["fields"].get("description")
        )

        return {
            "key": issue["key"],
            "summary": issue["fields"]["summary"],
            "description": description,
            "status": issue["fields"]["status"]["name"]
        }

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )
        
        
@app.get("/github/repository")
async def github_repository():

    try:

        repository = await get_repository()

        return {
            "name": repository["name"],
            "full_name": repository["full_name"],
            "private": repository["private"],
            "default_branch": repository["default_branch"],
            "html_url": repository["html_url"]
        }

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )
        
@app.get("/github/file")
async def github_file(path: str):

    try:

        file = await get_file_content(path)

        return file

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )

@app.get("/github/tree")
async def github_tree():

    try:

        tree = await get_repository_tree()

        files = [
            item["path"]
            for item in tree["tree"]
            if item["type"] == "blob"
        ]

        repository = await get_repository()

        return {
            "repository": repository["name"],
            "branch": repository["default_branch"],
            "files": files
        }

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )
        
@app.post("/github/branch")
async def github_branch(
    branch_name: str,
    base_branch: str = "main",
):
    try:
        result = await create_branch(
            branch_name,
            base_branch
        )

        return result

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )
@app.put("/github/file")
async def github_update_file(request: UpdateFileRequest):
    try:
        result = await update_file(
            file_path=request.path,
            content=request.content,
            branch=request.branch,
            commit_message=request.message,
        )

        return result

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )
        
@app.post("/ai/analyze")
async def ai_analyze(request: AIAnalysisRequest):
    try:
        graph = create_agent_graph()

        result = await graph.ainvoke({
            "issue_key": request.issue_key,
            "summary": request.summary,
            "description": request.description,
        })

        return {
            "issue_key": result["issue_key"],
            "analysis": result.get("analysis"),
            "requirements": result.get("requirements", []),
            "potential_files": result.get("potential_files", []),
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e),
        )
        
@app.post("/ai/analyze/{issue_key}")
async def analyze_jira_issue(issue_key: str):
    try:
        # --------------------------------
        # 1. Get Jira ticket
        # --------------------------------
        issue = await get_jira_issue(issue_key)

        description = extract_adf_text(
            issue["fields"].get("description")
        )

        # --------------------------------
        # 2. Get GitHub repository
        # --------------------------------
        repository = await get_repository_tree()

        repository_files = [
            item["path"]
            for item in repository["tree"]
            if item["type"] == "blob"
        ]

        # --------------------------------
        # 3. Create LangGraph
        # --------------------------------
        graph = create_agent_graph()

        # --------------------------------
        # 4. Run AI analysis
        # --------------------------------
        result = await graph.ainvoke({
            "issue_key": issue["key"],
            "summary": issue["fields"]["summary"],
            "description": description,
            "repository_files": repository_files,
        })

        # --------------------------------
        # 5. Return result
        # --------------------------------
        return {
            "issue_key": result["issue_key"],
            "summary": issue["fields"]["summary"],
            "analysis": result.get("analysis"),
            "requirements": result.get("requirements", []),
            "potential_files": result.get(
                "potential_files",
                []
            ),
            "source_files": result.get(
                "source_files",
                {}
            ),
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e),
        )
@app.post("/github/apply-changes")
async def github_apply_changes(
    request: ApplyCodeChangesRequest
):
    print("======================================")
    print("APPLY CODE CHANGES")
    print("Branch:", request.branch)
    print("Issue:", request.issue_key)
    print("Changes:", len(request.changes))
    print("======================================")

    try:
        if not request.branch:
            raise HTTPException(
                status_code=400,
                detail="Branch is required."
            )

        if not request.changes:
            raise HTTPException(
                status_code=400,
                detail="No code changes provided."
            )

        commit_message = (
            f"{request.issue_key}: Implement requested changes"
        )

        result = await commit_multiple_files(
            branch=request.branch,
            changes=[
                change.model_dump()
                for change in request.changes
            ],
            commit_message=commit_message,
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
        raise HTTPException(
            status_code=e.response.status_code,
            detail=e.response.text,
        )

    except HTTPException:
        raise

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e),
        )

@app.post("/github/test")
async def test_github_branch(branch: str):
    try:
        result = await run_branch_tests(branch)

        return {
            "branch": branch,
            **result,
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e),
        )
        
@app.post("/jira/create")
async def create_jira(request: CreateJiraRequest):
    try:
        requirement = request.requirement.strip()

        if not requirement:
            raise HTTPException(
                status_code=400,
                detail="Requirement cannot be empty.",
            )

        # Create initial LangGraph state
        state = {
            "raw_requirement": requirement,
        }

        # Structure requirement using Ollama
        result = await structure_requirement(state)

        # Create Jira ticket
        jira_issue = await create_jira_issue(
            summary=result["summary"],
            description=result["description"],
            acceptance_criteria=result.get(
                "acceptance_criteria",
                [],
            ),
            technical_notes=result.get(
                "technical_notes",
                [],
            ),
            test_requirements=result.get(
                "test_requirements",
                [],
            ),
        )

        return {
            "key": jira_issue["key"],
            "id": jira_issue["id"],
            "self": jira_issue["self"],
            "summary": result["summary"],
            "description": result["description"],
            "acceptance_criteria": result.get(
                "acceptance_criteria",
                [],
            ),
            "technical_notes": result.get(
                "technical_notes",
                [],
            ),
            "test_requirements": result.get(
                "test_requirements",
                [],
            ),
            "status": "To Do",
        }

    except httpx.HTTPStatusError as e:
        raise HTTPException(
            status_code=e.response.status_code,
            detail=e.response.text,
        )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e),
        )
        
@app.get("/jira/{issue_key}/transitions")
async def jira_transitions(issue_key: str):
    try:
        result = await get_jira_transitions(
            issue_key
        )

        return {
            "issue_key": issue_key,
            "transitions": [
                {
                    "id": transition["id"],
                    "name": transition["name"],
                    "to": transition.get("to", {}).get(
                        "name"
                    ),
                }
                for transition in result.get(
                    "transitions",
                    []
                )
            ],
        }

    except httpx.HTTPStatusError as e:
        raise HTTPException(
            status_code=e.response.status_code,
            detail=e.response.text,
        )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e),
        )

@app.post("/jira/{issue_key}/in-progress")
async def jira_in_progress(issue_key: str):
    try:
        result = await move_jira_issue_to_in_progress(
            issue_key
        )

        return result

    except httpx.HTTPStatusError as e:
        raise HTTPException(
            status_code=e.response.status_code,
            detail=e.response.text,
        )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e),
        )
        
def generate_branch_name(issue_key: str, summary: str) -> str:
    slug = summary.lower()

    slug = re.sub(
        r"[^a-z0-9]+",
        "-",
        slug,
    )

    slug = slug.strip("-")

    slug = slug[:50].rstrip("-")

    return f"feature/{issue_key.lower()}-{slug}"

@app.post("/github/feature-branch")
async def github_feature_branch(
    request: CreateFeatureBranchRequest,
):
    try:
        branch_name = generate_branch_name(
            request.issue_key,
            request.summary,
        )

        result = await create_branch(
            branch_name=branch_name,
            base_branch="main",
        )

        return {
            "issue_key": request.issue_key,
            "branch": branch_name,
            "base_branch": "main",
            "sha": result.get("sha"),
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e),
        )
@app.post("/ai/analyze-code")
async def analyze_code(request: AnalyzeCodeRequest):

    print("======================================")
    print("AI ANALYZE ENDPOINT CALLED")
    print("Issue:", request.issue_key)
    print("Repository files:", len(request.repository_files))
    print("======================================")

    try:
        state = {
            "issue_key": request.issue_key,
            "summary": request.summary,
            "description": request.description,
            "acceptance_criteria": request.acceptance_criteria,
            "technical_notes": request.technical_notes,
            "test_requirements": request.test_requirements,
            "repository_files": request.repository_files,
        }

        print("STATE CREATED")
        print("Starting agent graph...")

        result = await agent_graph.ainvoke(state)

        print("AGENT GRAPH FINISHED")
        print("Analysis:", result.get("analysis"))
        print(
            "Potential files:",
            result.get("potential_files")
        )
        print(
            "Source files:",
            list(result.get("source_files", {}).keys())
        )
        print(
            "Code changes:",
            len(result.get("code_changes", []))
        )

        return {
            "issue_key": request.issue_key,
            "analysis": result.get("analysis", ""),
            "requirements": result.get("requirements", []),
            "potential_files": result.get("potential_files", []),
            "file_actions": result.get("file_actions", []),
            "source_files": result.get("source_files", {}),
            "code_changes": result.get("code_changes", []),
        }

    except Exception as e:
        print("AI ANALYSIS ERROR:", str(e))
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )
        
@app.post("/github/apply-changes")
async def github_apply_changes(
    request: ApplyCodeChangesRequest,
):
    try:
        if not request.branch:
            raise HTTPException(
                status_code=400,
                detail="Branch is required.",
            )

        if not request.changes:
            raise HTTPException(
                status_code=400,
                detail="No code changes provided.",
            )

        commit_message = (
            f"{request.issue_key}: "
            "Implement requested changes"
        )

        result = await commit_multiple_files(
            branch=request.branch,
            changes=request.changes,
            commit_message=commit_message,
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
        raise HTTPException(
            status_code=e.response.status_code,
            detail=e.response.text,
        )

    except HTTPException:
        raise

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e),
        )
        
class CreatePullRequestRequest(BaseModel):
    issue_key: str
    summary: str
    description: str
    branch: str
    commit_sha: str


@app.post("/github/pull-request")
async def github_pull_request(
    request: CreatePullRequestRequest
):
    try:
        title = (
            f"{request.issue_key}: "
            f"{request.summary}"
        )

        body = f"""
## Jira Ticket

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

        return {
            "success": True,
            "issue_key": request.issue_key,
            "pull_request": result,
        }

    except httpx.HTTPStatusError as e:
        raise HTTPException(
            status_code=e.response.status_code,
            detail=e.response.text,
        )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e),
        )
        
@app.post("/jira/{issue_key}/code-review")
async def jira_code_review(issue_key: str):
    try:
        result = await move_jira_issue_to_code_review(
            issue_key
        )

        return result

    except httpx.HTTPStatusError as e:
        raise HTTPException(
            status_code=e.response.status_code,
            detail=e.response.text,
        )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e),
        )