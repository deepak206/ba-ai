from pydantic import BaseModel, Field

class CodeChange(BaseModel):
    file: str
    action: str
    reason: str = ""
    changes: list[str] = Field(default_factory=list)
    new_content: str

class ApplyCodeChangesRequest(BaseModel):
    branch: str
    issue_key: str
    changes: list[CodeChange]

class UpdateFileRequest(BaseModel):
    path: str
    content: str
    branch: str
    message: str

class CreateFeatureBranchRequest(BaseModel):
    issue_key: str
    summary: str

class FileChange(BaseModel):
    path: str
    content: str
    message: str

class CreatePullRequestRequest(BaseModel):
    issue_key: str
    summary: str
    description: str
    branch: str
    commit_sha: str
