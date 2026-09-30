from pydantic import BaseModel, Field

class AIAnalysisRequest(BaseModel):
    issue_key: str
    summary: str
    description: str

class AnalyzeCodeRequest(BaseModel):
    issue_key: str
    summary: str
    description: str
    acceptance_criteria: list[str] = Field(default_factory=list)
    technical_notes: list[str] = Field(default_factory=list)
    test_requirements: list[str] = Field(default_factory=list)
    repository_files: list[str]
