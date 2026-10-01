from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.routes import ai, github, jira

app = FastAPI(title="AI Development Agent", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(jira.router)
app.include_router(github.router)
app.include_router(ai.router)

@app.get("/")
def root():
    return {"message": "AI Development Agent API is running"}
