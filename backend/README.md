# AI Development Agent — Backend

FastAPI backend for the AI Development Agent.

The backend manages Jira, GitHub, AI code analysis, repository analysis, code generation, Git commits, and Pull Request creation.

---

## Technology Stack

- Python 3.x
- FastAPI
- Uvicorn
- LangGraph
- LangChain
- LangChain Ollama
- Ollama
- HTTPX
- Pydantic

AI model:

```text
qwen2.5-coder
```

---

## Backend Structure

```text
backend/
│
├── main.py
├── jira_service.py
├── github_service.py
├── test_service.py
├── .env
├── .gitignore
│
├── ai/
│   ├── __init__.py
│   ├── state.py
│   ├── nodes.py
│   └── graph.py
│
└── venv/
```

---

## AI Graph

The LangGraph workflow is:

```text
START
  ↓
analyze_requirement
  ↓
read_source_files
  ↓
generate_code_changes
  ↓
END
```

### `analyze_requirement`

Analyzes:

- Jira summary
- Jira description
- Acceptance criteria
- Technical notes
- Test requirements
- Repository file list

Produces:

- implementation analysis
- requirements
- potential files
- file actions

---

### `read_source_files`

Reads source files from GitHub for files that already exist.

New files do not need to be read because they will be created by the code-generation step.

---

### `generate_code_changes`

Generates complete source code for:

```text
create
modify
```

Every generated change contains:

```json
{
  "file": "src/App.jsx",
  "action": "modify",
  "reason": "Update application component",
  "changes": [
    "Add requested functionality"
  ],
  "new_content": "complete file content"
}
```

The backend validates generated changes before returning them to the frontend.

---

## Environment Setup

Create a virtual environment:

```bash
python -m venv venv
```

Activate on Windows:

```bash
venv\Scripts\activate
```

Install dependencies:

```bash
pip install fastapi uvicorn httpx python-dotenv
pip install langgraph langchain langchain-ollama
```

---

## Ollama

Install Ollama on Windows and make sure it is running.

Check:

```bash
ollama list
```

Install the model:

```bash
ollama pull qwen2.5-coder
```

Test:

```bash
ollama run qwen2.5-coder
```

---

## Environment Variables

Create:

```text
backend/.env
```

Example:

```env
JIRA_BASE_URL=https://your-company.atlassian.net
JIRA_EMAIL=your-email@example.com
JIRA_API_TOKEN=your-jira-api-token

GITHUB_TOKEN=your-github-token
GITHUB_OWNER=your-github-username-or-organization
GITHUB_REPO=your-repository-name
```

---

## Start Backend

From the backend directory:

```bash
venv\Scripts\activate
```

Then:

```bash
python -m uvicorn main:app --reload
```

Server:

```text
http://127.0.0.1:8000
```

Swagger:

```text
http://127.0.0.1:8000/docs
```

---

## API Endpoints

### Jira

Create Jira ticket:

```text
POST /jira/create
```

Get Jira issue:

```text
GET /jira/{issue_key}
```

Get transitions:

```text
GET /jira/{issue_key}/transitions
```

Move ticket to In Progress:

```text
POST /jira/{issue_key}/in-progress
```

---

### GitHub

Get repository:

```text
GET /github/repository
```

Get repository tree:

```text
GET /github/tree
```

Get file:

```text
GET /github/file/{file_path}
```

Create feature branch:

```text
POST /github/feature-branch
```

Apply approved code changes:

```text
POST /github/apply-changes
```

Create Pull Request:

```text
POST /github/pull-request
```

---

### AI

Analyze repository and generate code changes:

```text
POST /ai/analyze-code
```

---

## Apply Code Changes

The endpoint accepts:

```json
{
  "branch": "feature/kan-12-example",
  "issue_key": "KAN-12",
  "changes": [
    {
      "file": "src/App.jsx",
      "action": "modify",
      "reason": "Implement requested functionality",
      "changes": [
        "Update application component"
      ],
      "new_content": "complete file content"
    }
  ]
}
```

All approved changes are applied as **one Git commit**.

Commit message:

```text
KAN-12: Implement requested changes
```

---

## Pull Request

After the commit is created, the frontend can request a Pull Request.

The response contains:

```json
{
  "success": true,
  "issue_key": "KAN-12",
  "pull_request": {
    "number": 15,
    "title": "KAN-12: Example requirement",
    "url": "https://github.com/...",
    "state": "open",
    "head": "feature/kan-12-example",
    "base": "main"
  }
}
```

---

## CORS

The backend allows the Vite frontend:

```text
http://localhost:5173
```

Example:

```python
add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

---

## Development Rules

The existing frontend project uses:

```text
JavaScript
JSX
React
```

The AI should therefore generate:

```text
.js
.jsx
```

and should not generate:

```text
.ts
.tsx
tsconfig.json
```

unless the requirement explicitly asks for TypeScript.

The AI should also avoid creating unnecessary:

```text
.eslintrc.js
.prettierrc
README.md
```

files unless required.

---

## Security

Never expose these values to the frontend:

```text
JIRA_API_TOKEN
GITHUB_TOKEN
```

They must remain in the backend `.env`.

Never commit:

```text
.env
```

to Git.

---

## Debugging

Run with:

```bash
python -m uvicorn main:app --reload
```

Check the terminal for:

```text
AI ANALYZE ENDPOINT CALLED
STATE CREATED
Starting agent graph...
AGENT GRAPH FINISHED
```

For GitHub changes:

```text
APPLY CODE CHANGES
```

For PR creation:

```text
PR RESPONSE
```

Swagger can be used to test individual endpoints:

```text
http://127.0.0.1:8000/docs
```