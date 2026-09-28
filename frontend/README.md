# AI Development Agent — Frontend

React frontend for the AI Development Agent.

The frontend provides the user interface for entering requirements, reviewing Jira tickets, approving development actions, reviewing AI-generated code, approving commits, and creating Pull Requests.

---

## Technology Stack

- React
- Vite
- JavaScript
- JSX
- Tailwind CSS
- Framer Motion

---

## Frontend Structure

```text
frontend/
│
├── package.json
├── vite.config.js
│
└── src/
    │
    ├── App.jsx
    ├── main.jsx
    ├── index.css
    │
    ├── components/
    │   │
    │   ├── Requirement/
    │   │   └── RequirementForm.jsx
    │   │
    │   ├── Jira/
    │   │   ├── JiraTicket.jsx
    │   │   ├── JiraTicketCreated.jsx
    │   │   └── JiraStatusApproval.jsx
    │   │
    │   ├── GitHub/
    │   │   ├── RepositoryInfo.jsx
    │   │   ├── BranchManager.jsx
    │   │   ├── BranchApproval.jsx
    │   │   ├── FileList.jsx
    │   │   ├── FileViewer.jsx
    │   │   ├── TestRunner.jsx
    │   │   └── PullRequestApproval.jsx
    │   │
    │   └── AI/
    │       ├── CodeAnalysis.jsx
    │       └── CodeReview.jsx
    │
    └── services/
        └── api.js
```

---

## Installation

From the frontend directory:

```bash
npm install
```

---

## Start Development Server

```bash
npm run dev
```

Frontend:

```text
http://localhost:5173
```

---

## Build Production Version

```bash
npm run build
```

Preview the production build:

```bash
npm run preview
```

---

## Tailwind CSS

The project uses Tailwind CSS with the Vite plugin.

`vite.config.js`:

```javascript
import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";
import tailwindcss from "@tailwindcss/vite";

export default defineConfig({
  plugins: [react(), tailwindcss()],
});
```

`src/index.css`:

```css
@import "tailwindcss";

body {
  margin: 0;
  font-family: Inter, system-ui, sans-serif;
}
```

---

## Backend Connection

The frontend communicates with:

```text
http://127.0.0.1:8000
```

The API configuration is in:

```text
src/services/api.js
```

Example:

```javascript
const API_BASE_URL = "http://127.0.0.1:8000";
```

---

## Main Workflow

### Step 1 — Requirement

User enters a raw requirement.

```text
RequirementForm
        ↓
Create Jira ticket
```

---

### Step 2 — Jira

The application displays the created Jira ticket.

The user can approve moving it to:

```text
In Progress
```

---

### Step 3 — Feature Branch

The application creates a branch such as:

```text
feature/kan-12-set-up-react-frontend-with-vite-and-tailwind-css
```

The branch is created from:

```text
main
```

---

### Step 4 — Repository

The frontend loads the GitHub repository tree.

The repository file list is passed to the AI backend.

Example:

```javascript
const result = await getRepositoryTree();
```

The repository files are then passed to:

```javascript
analyzeCodeChanges({
  issueKey,
  summary,
  description,
  acceptanceCriteria,
  technicalNotes,
  testRequirements,
  repositoryFiles,
});
```

---

### Step 5 — AI Code Analysis

The AI analyzes:

- Requirement
- Acceptance criteria
- Technical notes
- Repository files
- Existing source code

The result contains:

```text
analysis
requirements
potential_files
file_actions
source_files
code_changes
```

---

### Step 6 — Code Review

The frontend displays:

```text
Original Code
        ↓
Proposed Code
```

The user can:

```text
Approve
```

or:

```text
Request Changes
```

No GitHub changes are made before approval.

---

### Step 7 — Commit

After approval:

```text
POST /github/apply-changes
```

The backend creates one atomic Git commit.

Example:

```text
KAN-12: Implement requested changes
```

The UI displays:

```text
Commit SHA
Commit URL
Files Changed
Branch
```

---

### Step 8 — Pull Request

The user can select:

```text
Raise Pull Request
```

The backend creates the PR.

The response structure is:

```json
{
  "success": true,
  "issue_key": "KAN-12",
  "pull_request": {
    "number": 15,
    "title": "KAN-12: Example",
    "url": "https://github.com/...",
    "state": "open",
    "head": "feature/kan-12-example",
    "base": "main"
  }
}
```

The UI displays:

```text
PR: #15
Branch: feature/kan-12-example
Target: main
View Pull Request →
```

---

## API Service Functions

`src/services/api.js` contains functions for:

```text
createJiraIssue()
moveJiraIssueToInProgress()
createFeatureBranch()
getRepositoryTree()
analyzeCodeChanges()
applyCodeChanges()
createPullRequest()
```

---

## UI Components

### Requirement

```text
RequirementForm.jsx
```

Collects the user's requirement.

### Jira

```text
JiraTicketCreated.jsx
JiraStatusApproval.jsx
```

Displays Jira information and handles status approval.

### GitHub

```text
RepositoryInfo.jsx
BranchManager.jsx
BranchApproval.jsx
FileList.jsx
FileViewer.jsx
PullRequestApproval.jsx
```

Handles repository and GitHub workflow.

### AI

```text
CodeAnalysis.jsx
CodeReview.jsx
```

Displays AI analysis and proposed code changes.

---

## State Flow

The main application state is managed in:

```text
App.jsx
```

Important state includes:

```javascript
jiraTicket
developmentBranch
repository
codeAnalysis
codeReviewStatus
commitResult
pullRequestResult
```

The overall state flow is:

```text
jiraTicket
     ↓
developmentBranch
     ↓
repository
     ↓
codeAnalysis
     ↓
codeReviewStatus
     ↓
commitResult
     ↓
pullRequestResult
```

---

## Human Approval

The frontend intentionally requires user approval before:

```text
Move Jira ticket
       ↓
Create branch
       ↓
Apply code
       ↓
Create Pull Request
```

This prevents the AI from making uncontrolled repository changes.

---

## Development Rules

Use JavaScript/JSX:

```text
.js
.jsx
```

Do not introduce TypeScript files into this project unless the project is intentionally migrated.

Avoid unnecessary:

```text
.ts
.tsx
tsconfig.json
```

files.

---

## Troubleshooting

### Backend connection error

Make sure FastAPI is running:

```bash
cd backend
python -m uvicorn main:app --reload
```

Check:

```text
http://127.0.0.1:8000/docs
```

---

### Frontend not starting

Run:

```bash
npm install
npm run dev
```

---

### AI analysis is empty

Check that the repository has been loaded before calling:

```text
POST /ai/analyze-code
```

The request should contain:

```json
{
  "repository_files": [
    "README.md",
    "src/App.jsx",
    "src/main.jsx"
  ]
}
```

---

### Pull Request information is empty

The PR API response is nested:

```javascript
result.pull_request.number
result.pull_request.head
result.pull_request.base
result.pull_request.url
```

Not:

```javascript
result.number
result.branch
result.base
```

---

## Production Considerations

Before production deployment:

- Move API URL to environment variables
- Add authentication
- Secure Jira credentials
- Secure GitHub credentials
- Add proper error boundaries
- Add loading/error states
- Add automated frontend tests
- Add backend API tests
- Add code-generation validation
- Add repository permission controls
- Add audit logging