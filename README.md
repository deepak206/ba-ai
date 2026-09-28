# AI Development Agent

An AI-powered software development agent designed to connect **Jira business requirements** with **GitHub source code** and automate parts of the software development lifecycle.

The project uses **React**, **FastAPI**, **LangGraph**, **MongoDB**, and **Ollama**.

---

## 🚀 Project Goal

The goal is to build an AI development workflow where a business user creates or provides a Jira requirement, and the agent can understand the requirement, inspect the relevant GitHub source code, create a development branch, make code changes, run tests, and move the change through DEV → UAT → PROD with human approval at important stages.

### Target Workflow

```text
Business User
      │
      ▼
    Jira
      │
      ▼
 React Frontend
      │
      ▼
 FastAPI Backend
      │
      ▼
 LangGraph AI Agent
      │
      ├──────────────► Jira
      │
      ├──────────────► GitHub
      │
      ▼
 Analyze Requirement
      │
      ▼
 Identify Relevant Files
      │
      ▼
 Create Feature Branch
      │
      ▼
 Modify Source Code
      │
      ▼
 Run Tests
      │
      ▼
 Deploy to DEV
      │
      ▼
 Business User Testing
      │
      ├── FAIL ──► Read Jira → Modify Code → Test Again
      │
      ▼
 UAT
      │
      ▼
 Production Deployment
      │
      ▼
 Manual Approval
```

---

# 🛠️ Technology Stack

## Frontend

- React
- Vite
- JavaScript
- Reusable React components

## Backend

- Python
- FastAPI
- HTTPX
- Python-dotenv

## AI

- LangGraph
- Ollama
- LLM models

## Data

- MongoDB

## Integrations

- Jira REST API
- GitHub REST API

---

# 📁 Project Structure

```text
ba-ai/
│
├── backend/
│   ├── main.py
│   ├── jira_service.py
│   ├── github_service.py
│   ├── .env
│   ├── .gitignore
│   └── venv/
│
└── frontend/
    ├── src/
    │   ├── components/
    │   │   ├── Jira/
    │   │   │   ├── JiraTicket.jsx
    │   │   │   └── JiraTicketForm.jsx
    │   │   │
    │   │   ├── GitHub/
    │   │   │   ├── RepositoryInfo.jsx
    │   │   │   ├── FileList.jsx
    │   │   │   └── FileViewer.jsx
    │   │   │
    │   │   └── common/
    │   │       └── Loading.jsx
    │   │
    │   ├── services/
    │   │   └── api.js
    │   │
    │   ├── App.jsx
    │   └── main.jsx
    │
    ├── package.json
    └── vite.config.js
```

---

# ⚙️ Backend Setup

Navigate to the backend directory:

```bash
cd backend
```

Create a Python virtual environment:

```bash
python -m venv venv
```

Activate it on Windows:

```bash
.\venv\Scripts\activate
```

Install dependencies:

```bash
pip install fastapi uvicorn httpx python-dotenv
```

Start the FastAPI server:

```bash
python -m uvicorn main:app --reload
```

The backend will be available at:

```text
http://127.0.0.1:8000
```

Swagger API documentation:

```text
http://127.0.0.1:8000/docs
```

---

# 🔐 Environment Configuration

Create a `.env` file inside the `backend` directory.

```env
JIRA_BASE_URL=https://your-company.atlassian.net
JIRA_EMAIL=your-email@example.com
JIRA_API_TOKEN=your-jira-api-token

GITHUB_TOKEN=your-github-token
GITHUB_OWNER=your-github-username-or-organization
GITHUB_REPO=your-repository-name
```

### Important

Never commit `.env` to GitHub.

The `.gitignore` should contain:

```gitignore
venv/
.env
__pycache__/
```

---

# 💻 Frontend Setup

Navigate to the frontend directory:

```bash
cd frontend
```

Install dependencies:

```bash
npm install
```

Start the development server:

```bash
npm run dev
```

The frontend will normally be available at:

```text
http://localhost:5173
```

---

# 🔌 Current API Endpoints

## Jira

### Get Jira Issue

```http
GET /jira/{issue_key}
```

Example:

```text
GET /jira/PROJ-123
```

Response:

```json
{
  "key": "PROJ-123",
  "summary": "Add search functionality",
  "description": "Add search functionality to the product page",
  "status": "To Do"
}
```

---

# 🐙 GitHub APIs

## Get Repository

```http
GET /github/repository
```

Returns information about the configured GitHub repository.

---

## Get Repository Tree

```http
GET /github/tree
```

Example response:

```json
{
  "repository": "my-project",
  "branch": "main",
  "files": [
    "package.json",
    "src/App.jsx",
    "src/components/Search.jsx",
    "src/services/api.js"
  ]
}
```

---

## Read GitHub File

```http
GET /github/file?path=src/App.jsx
```

Example response:

```json
{
  "path": "src/App.jsx",
  "content": "import React from 'react';..."
}
```

---

# 🖥️ Current Frontend Features

The React application currently provides:

### Jira

- Enter Jira ticket ID
- Retrieve Jira ticket
- Display:
  - Ticket ID
  - Summary
  - Status
  - Description

### GitHub

- Read configured repository
- Display repository name
- Display default branch
- Display repository file list
- Select a file
- Read and display source code

---

# 🧩 Component Architecture

The frontend is intentionally divided into reusable components.

### JiraTicketForm

Responsible for:

- Jira ticket input
- Read Jira button
- Loading state

### JiraTicket

Responsible for:

- Displaying Jira information

### RepositoryInfo

Responsible for:

- Repository name
- Branch
- File count

### FileList

Responsible for:

- Displaying repository files
- Selecting a file

### FileViewer

Responsible for:

- Displaying selected source code
- Loading state
- Error state

### API Service

All backend communication is kept inside:

```text
src/services/api.js
```

This keeps API logic separate from UI components.

---

# 🤖 Planned AI Workflow

The project will gradually evolve into an AI-driven development agent.

## Phase 1 — Integrations

- [x] FastAPI setup
- [x] Jira API integration
- [x] React frontend
- [x] GitHub repository integration
- [x] Read GitHub repository tree
- [x] Read GitHub files

## Phase 2 — Git Operations

- [ ] Create GitHub feature branch
- [ ] Read files from feature branch
- [ ] Modify source code
- [ ] Commit changes
- [ ] Push changes
- [ ] Create Pull Request

## Phase 3 — AI Agent

- [ ] Install Ollama
- [ ] Connect LLM
- [ ] Add LangGraph
- [ ] Create agent state
- [ ] Jira requirement analysis
- [ ] Identify relevant source files
- [ ] Generate code changes
- [ ] Review generated changes
- [ ] Human approval

## Phase 4 — Testing

- [ ] Detect project type
- [ ] Install project dependencies
- [ ] Run existing tests
- [ ] Generate tests when required
- [ ] Analyze test failures
- [ ] Fix code based on test results
- [ ] Repeat until tests pass

## Phase 5 — Deployment

- [ ] DEV deployment
- [ ] Business User notification
- [ ] Business User testing
- [ ] Jira feedback processing
- [ ] UAT deployment
- [ ] UAT approval
- [ ] Production deployment
- [ ] Manual production approval

---

# 🧠 LangGraph Agent Concept

The future agent will use a state-based workflow similar to:

```text
START
  │
  ▼
Read Jira
  │
  ▼
Analyze Requirement
  │
  ▼
Find Relevant Files
  │
  ▼
Read Source Code
  │
  ▼
Generate Code Changes
  │
  ▼
Human Review
  │
  ├── Reject ──► Revise
  │
  ▼
Create Branch
  │
  ▼
Apply Changes
  │
  ▼
Run Tests
  │
  ├── Fail ──► Analyze Failure
  │              │
  │              └──► Fix Code
  │
  ▼
Deploy DEV
  │
  ▼
Business Testing
  │
  ├── Fail ──► Jira Feedback
  │              │
  │              └──► Fix Code
  │
  ▼
UAT
  │
  ▼
Manual Production Approval
  │
  ▼
PRODUCTION
```

---

# 🔒 Safety and Approval Model

The agent should not have unrestricted authority over production.

Recommended controls:

- AI changes are created on a feature branch.
- `main` should remain protected.
- Code changes should be reviewable before merging.
- Automated tests must run before deployment.
- DEV deployment can be automated.
- Business User testing should require confirmation.
- UAT deployment should require approval.
- Production deployment should remain manually approved.
- GitHub and Jira credentials must remain in backend environment variables.
- API tokens must never be exposed to the React frontend.

---

# 🎯 Long-Term Goal

The final system should allow a Business User to provide a requirement such as:

```text
PROJ-123

Add a search filter to the customer list.
Users should be able to search customers by name and email.
```

The AI Development Agent should then:

```text
1. Read Jira
       ↓
2. Understand requirement
       ↓
3. Inspect GitHub repository
       ↓
4. Identify relevant files
       ↓
5. Create feature branch
       ↓
6. Modify code
       ↓
7. Generate/update tests
       ↓
8. Run tests
       ↓
9. Deploy DEV
       ↓
10. Notify Business User
       ↓
11. Process feedback
       ↓
12. Deploy UAT
       ↓
13. Obtain approval
       ↓
14. Manual production deployment
```

---

# 📌 Development Approach

The project is being developed incrementally.

Each major capability is implemented and tested independently before moving to the next stage.

Current development priority:

```text
Jira
  ↓
GitHub
  ↓
Branch Creation
  ↓
Code Modification
  ↓
Testing
  ↓
AI Agent
  ↓
Deployment
```

---

# 📄 License

This project is currently intended for development and experimentation.