from typing import TypedDict


class AgentState(TypedDict, total=False):
    issue_key: str
    summary: str
    description: str
    raw_requirement: str

    repository_files: list[str]
    repository_branch: str

    analysis: str
    requirements: list[str]
    potential_files: list[str]

    file_actions: list[dict]
    source_files: dict[str, str]

    code_changes: list[dict]

    acceptance_criteria: list[str]
    technical_notes: list[str]
    test_requirements: list[str]