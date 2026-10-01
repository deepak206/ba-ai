from fastapi import APIRouter, HTTPException

from schemas.ai import AIAnalysisRequest, AnalyzeCodeRequest
from services.ai_service import analyze_issue, analyze_code

router = APIRouter(prefix="/ai", tags=["AI"])

@router.post("/analyze")
async def ai_analyze(request: AIAnalysisRequest):
    try:
        return await analyze_issue(request)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/analyze/{issue_key}")
async def analyze_jira_issue(issue_key: str):
    try:
        return await analyze_issue(issue_key=issue_key)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/analyze-code")
async def analyze_code_endpoint(request: AnalyzeCodeRequest):
    try:
        return await analyze_code(request)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
