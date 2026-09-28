from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware


from jira_service import (
    get_jira_issue,
    extract_adf_text
)
from github_service import (
    get_repository,
    get_file_content,
    get_repository_tree
)

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