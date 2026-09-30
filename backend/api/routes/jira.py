from fastapi import APIRouter, HTTPException
import httpx

from schemas.jira import CreateJiraRequest
from jira_service import (
    get_jira_issue,
    create_jira_issue,
    extract_adf_text,
    get_jira_transitions,
    move_jira_issue_to_in_progress,
    move_jira_issue_to_code_review,
)
from services.ai_service import structure_jira_requirement

router = APIRouter(prefix="/jira", tags=["Jira"])

@router.get("/{issue_key}")
async def get_jira(issue_key: str):
    try:
        issue = await get_jira_issue(issue_key)
        description = extract_adf_text(issue["fields"].get("description"))
        return {
            "key": issue["key"],
            "summary": issue["fields"]["summary"],
            "description": description,
            "status": issue["fields"]["status"]["name"],
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/create")
async def create_jira(request: CreateJiraRequest):
    try:
        requirement = request.requirement.strip()
        if not requirement:
            raise HTTPException(status_code=400, detail="Requirement cannot be empty.")

        result = await structure_jira_requirement(requirement)

        jira_issue = await create_jira_issue(
            summary=result["summary"],
            description=result["description"],
            acceptance_criteria=result.get("acceptance_criteria", []),
            technical_notes=result.get("technical_notes", []),
            test_requirements=result.get("test_requirements", []),
        )

        return {
            "key": jira_issue["key"],
            "id": jira_issue["id"],
            "self": jira_issue["self"],
            **result,
            "status": "To Do",
        }
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=e.response.status_code, detail=e.response.text)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{issue_key}/transitions")
async def jira_transitions(issue_key: str):
    try:
        result = await get_jira_transitions(issue_key)
        return {
            "issue_key": issue_key,
            "transitions": [
                {
                    "id": t["id"],
                    "name": t["name"],
                    "to": t.get("to", {}).get("name"),
                }
                for t in result.get("transitions", [])
            ],
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/{issue_key}/in-progress")
async def jira_in_progress(issue_key: str):
    try:
        return await move_jira_issue_to_in_progress(issue_key)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/{issue_key}/code-review")
async def jira_code_review(issue_key: str):
    try:
        return await move_jira_issue_to_code_review(issue_key)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
