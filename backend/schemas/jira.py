from pydantic import BaseModel

class CreateJiraRequest(BaseModel):
    requirement: str
