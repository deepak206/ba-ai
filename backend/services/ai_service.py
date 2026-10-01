from ai.nodes import structure_requirement
from ai.graph import create_agent_graph
from jira_service import get_jira_issue, extract_adf_text
from github_service import get_repository_tree

async def structure_jira_requirement(requirement: str):
    return await structure_requirement({"raw_requirement": requirement})

async def analyze_issue(request=None, issue_key=None):
    if request is not None:
        graph = create_agent_graph()
        result = await graph.ainvoke({
            "issue_key": request.issue_key,
            "summary": request.summary,
            "description": request.description,
        })
        return {
            "issue_key": result["issue_key"],
            "analysis": result.get("analysis"),
            "requirements": result.get("requirements", []),
            "potential_files": result.get("potential_files", []),
        }

    issue = await get_jira_issue(issue_key)
    description = extract_adf_text(issue["fields"].get("description"))
    repository = await get_repository_tree()
    repository_files = [item["path"] for item in repository["tree"] if item["type"] == "blob"]

    graph = create_agent_graph()
    result = await graph.ainvoke({
        "issue_key": issue["key"],
        "summary": issue["fields"]["summary"],
        "description": description,
        "repository_files": repository_files,
    })

    return {
        "issue_key": result["issue_key"],
        "summary": issue["fields"]["summary"],
        "analysis": result.get("analysis"),
        "requirements": result.get("requirements", []),
        "potential_files": result.get("potential_files", []),
        "source_files": result.get("source_files", {}),
    }

async def analyze_code(request):
    graph = create_agent_graph()
    result = await graph.ainvoke({
        "issue_key": request.issue_key,
        "summary": request.summary,
        "description": request.description,
        "acceptance_criteria": request.acceptance_criteria,
        "technical_notes": request.technical_notes,
        "test_requirements": request.test_requirements,
        "repository_files": request.repository_files,
    })
    return {
        "issue_key": request.issue_key,
        "analysis": result.get("analysis", ""),
        "requirements": result.get("requirements", []),
        "potential_files": result.get("potential_files", []),
        "file_actions": result.get("file_actions", []),
        "source_files": result.get("source_files", {}),
        "code_changes": result.get("code_changes", []),
    }
