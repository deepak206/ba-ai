import os
import httpx
from dotenv import load_dotenv

load_dotenv()

JIRA_BASE_URL = os.getenv("JIRA_BASE_URL")
JIRA_EMAIL = os.getenv("JIRA_EMAIL")
JIRA_API_TOKEN = os.getenv("JIRA_API_TOKEN")


JIRA_HEADERS = {
    "Accept": "application/json",
    "Content-Type": "application/json",
}


# ---------------------------------------------------------
# Get existing Jira issue
# ---------------------------------------------------------

async def get_jira_issue(issue_key: str):
    url = f"{JIRA_BASE_URL}/rest/api/3/issue/{issue_key}"

    async with httpx.AsyncClient() as client:
        response = await client.get(
            url,
            headers=JIRA_HEADERS,
            auth=(
                JIRA_EMAIL,
                JIRA_API_TOKEN,
            ),
        )

        response.raise_for_status()

        return response.json()


# ---------------------------------------------------------
# Create new Jira issue
# ---------------------------------------------------------

async def create_jira_issue(
    summary: str,
    description: str,
    acceptance_criteria: list[str] | None = None,
    technical_notes: list[str] | None = None,
    test_requirements: list[str] | None = None,
):
    url = f"{JIRA_BASE_URL}/rest/api/3/issue"

    acceptance_criteria = acceptance_criteria or []
    technical_notes = technical_notes or []
    test_requirements = test_requirements or []

    description_text = description

    if acceptance_criteria:
        description_text += "\n\nAcceptance Criteria:\n"

        for index, item in enumerate(
            acceptance_criteria,
            start=1,
        ):
            description_text += (
                f"{index}. {item}\n"
            )

    if technical_notes:
        description_text += "\nTechnical Notes:\n"

        for item in technical_notes:
            description_text += f"- {item}\n"

    if test_requirements:
        description_text += "\nTest Requirements:\n"

        for item in test_requirements:
            description_text += f"- {item}\n"

    payload = {
        "fields": {
            "project": {
                "key": "KAN"
            },
            "summary": summary,
            "description": {
                "type": "doc",
                "version": 1,
                "content": [
                    {
                        "type": "paragraph",
                        "content": [
                            {
                                "type": "text",
                                "text": description_text,
                            }
                        ],
                    }
                ],
            },
            "issuetype": {
                "name": "Task"
            },
        }
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(
            url,
            headers=JIRA_HEADERS,
            auth=(
                JIRA_EMAIL,
                JIRA_API_TOKEN,
            ),
            json=payload,
        )

        response.raise_for_status()

        return response.json()

def extract_adf_text(node):
    if not node:
        return ""

    if isinstance(node, dict):
        if node.get("type") == "text":
            return node.get("text", "")

        return "".join(
            extract_adf_text(child)
            for child in node.get("content", [])
        )

    if isinstance(node, list):
        return "".join(
            extract_adf_text(item)
            for item in node
        )

    return ""

async def get_jira_transitions(issue_key: str):
    url = (
        f"{JIRA_BASE_URL}/rest/api/3/issue/"
        f"{issue_key}/transitions"
    )

    async with httpx.AsyncClient() as client:
        response = await client.get(
            url,
            headers=JIRA_HEADERS,
            auth=(
                JIRA_EMAIL,
                JIRA_API_TOKEN,
            ),
        )

        response.raise_for_status()

        return response.json()
    
async def move_jira_issue_to_in_progress(
    issue_key: str,
):
    transitions = await get_jira_transitions(
        issue_key
    )

    available_transitions = transitions.get(
        "transitions",
        []
    )

    target_transition = None

    for transition in available_transitions:
        name = transition.get("name", "").strip().lower()

        if name == "in progress":
            target_transition = transition
            break

    if not target_transition:
        available_names = [
            transition.get("name")
            for transition in available_transitions
        ]

        raise ValueError(
            "In Progress transition is not available. "
            f"Available transitions: {available_names}"
        )

    transition_id = target_transition["id"]

    url = (
        f"{JIRA_BASE_URL}/rest/api/3/issue/"
        f"{issue_key}/transitions"
    )

    payload = {
        "transition": {
            "id": transition_id
        }
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(
            url,
            headers=JIRA_HEADERS,
            auth=(
                JIRA_EMAIL,
                JIRA_API_TOKEN,
            ),
            json=payload,
        )

        response.raise_for_status()

    return {
        "key": issue_key,
        "status": "In Progress",
        "transition_id": transition_id,
    }
    
async def create_pull_request(
    title: str,
    body: str,
    head: str,
    base: str = "main",
):
    url = (
        f"{GITHUB_API_URL}/repos/"
        f"{GITHUB_OWNER}/{GITHUB_REPO}/pulls"
    )

    payload = {
        "title": title,
        "body": body,
        "head": head,
        "base": base,
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(
            url,
            headers=GITHUB_HEADERS,
            json=payload,
        )

        response.raise_for_status()

        result = response.json()

    return {
        "number": result.get("number"),
        "title": result.get("title"),
        "url": result.get("html_url"),
        "state": result.get("state"),
        "head": result.get("head", {}).get("ref"),
        "base": result.get("base", {}).get("ref"),
    }