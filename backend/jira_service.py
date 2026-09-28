import os
import httpx
from dotenv import load_dotenv

load_dotenv()

JIRA_BASE_URL = os.getenv("JIRA_BASE_URL")
JIRA_EMAIL = os.getenv("JIRA_EMAIL")
JIRA_API_TOKEN = os.getenv("JIRA_API_TOKEN")


def extract_adf_text(node):
    """
    Convert Jira Atlassian Document Format (ADF)
    into plain text.
    """

    if not node:
        return ""

    if isinstance(node, str):
        return node

    result = []

    if node.get("type") == "text":
        result.append(node.get("text", ""))

    for child in node.get("content", []):
        result.append(extract_adf_text(child))

    if node.get("type") == "paragraph":
        result.append("\n")

    return "".join(result)


async def get_jira_issue(issue_key: str):

    url = f"{JIRA_BASE_URL}/rest/api/3/issue/{issue_key}"

    async with httpx.AsyncClient() as client:

        response = await client.get(
            url,
            auth=(JIRA_EMAIL, JIRA_API_TOKEN),
            headers={
                "Accept": "application/json"
            }
        )

        response.raise_for_status()

        return response.json()
  