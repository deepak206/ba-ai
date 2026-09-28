# AI Development Agent

An AI-powered software development agent that helps convert a raw software requirement into a Jira ticket, create a development branch, analyze the repository, generate code changes, allow human review, commit approved changes, and optionally raise a GitHub Pull Request.

The project uses **React + Vite** for the frontend, **FastAPI + LangGraph + Ollama** for the backend, and integrates with **Jira and GitHub**.

---

## Architecture

```text
                    ┌──────────────────────┐
                    │   User Requirement   │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │   React Frontend     │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │    FastAPI Backend   │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │    Ollama + LLM      │
                    └──────────┬───────────┘
                               │
              ┌────────────────┼────────────────┐
              ▼                ▼                ▼
           Jira             GitHub          Repository
              │                │                │
              └────────────────┼────────────────┘
                               │
                               ▼
                       Human Code Review
                               │
                    ┌──────────┴──────────┐
                    │                     │
                  Approve              Changes
                    │
                    ▼
               Git Commit
                    │
                    ▼
             Create Pull Request
```

---

## Development Workflow

```text
1. Enter requirement
        ↓
2. AI structures requirement
        ↓
3. Create Jira ticket
        ↓
4. User approves "Move to In Progress"
        ↓
5. Jira → In Progress
        ↓
6. User approves branch creation
        ↓
7. Create feature/KAN-XXX-... branch
        ↓
8. Load GitHub repository
        ↓
9. AI analyzes requirement
        ↓
10. AI identifies files
        ↓
11. AI reads source files
        ↓
12. AI generates code changes
        ↓
13. User reviews proposed changes
        ↓
14. Approve / Request Changes
        ↓
15. Apply approved changes
        ↓
16. One Git commit
        ↓
17. User approves Pull Request
        ↓
18. Create GitHub Pull Request
```

Human approval is required before important actions.

---

## Project Structure

```text
ba-ai/
│
├── README.md
│
├── backend/
│   ├── main.py
│   ├── jira_service.py
│   ├── github_service.py
│   ├── test_service.py
│   ├── .env
│   ├── .gitignore
│   │
│   ├── ai/
│   │   ├── __init__.py
│   │   ├── state.py
│   │   ├── nodes.py
│   │   └── graph.py
│   │
│   └── venv/
│
└── frontend/
    ├── package.json
    ├── vite.config.js
    └── src/
        ├── App.jsx
        ├── main.jsx
        ├── index.css
        │
        ├── components/
        │   ├── Requirement/
        │   ├── Jira/
        │   ├── GitHub/
        │   └── AI/
        │
        └── services/
            └── api.js
```

---

## Technology Stack

### Frontend

- React
- Vite
- JavaScript / JSX
- Tailwind CSS
- Framer Motion

### Backend

- Python
- FastAPI
- Uvicorn
- LangGraph
- LangChain
- LangChain Ollama
- HTTPX
- Pydantic

### AI

- Ollama
- Qwen 2.5 Coder

### Integrations

- Jira REST API
- GitHub REST API

---

## Running the Project

### Start Backend

```bash
cd backend
```

Activate virtual environment:

```bash
venv\Scripts\activate
```

Start FastAPI:

```bash
python -m uvicorn main:app --reload
```

Backend:

```text
http://127.0.0.1:8000
```

Swagger:

```text
http://127.0.0.1:8000/docs
```

---

### Start Frontend

Open another terminal:

```bash
cd frontend
```

Install dependencies:

```bash
npm install
```

Start Vite:

```bash
npm run dev
```

Frontend:

```text
http://localhost:5173
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

Never commit `.env` to Git.

---

## Important Safety Rules

The agent does not automatically:

- approve code
- merge Pull Requests
- deploy applications
- move tickets without approval
- commit code without human approval

The intended workflow is:

```text
AI proposes
   ↓
Human reviews
   ↓
Human approves
   ↓
System executes
```

---

## Future Improvements

Planned capabilities:

- MongoDB agent state persistence
- Conversation/session management
- Improved code analysis
- Repository-aware RAG
- Automated test generation
- Test execution
- Code quality checks
- Jira comments/status synchronization
- GitHub PR review
- PR feedback → AI code revision
- Multi-agent development workflow
- Docker support
- Authentication and user management