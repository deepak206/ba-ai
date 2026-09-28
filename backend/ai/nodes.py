import json

from langchain_ollama import ChatOllama

from .state import AgentState
from github_service import get_file_content


llm = ChatOllama(
    model="qwen2.5-coder",
    temperature=0,
)


# ============================================================
# STEP 1
# Structure raw requirement
# ============================================================

async def structure_requirement(state: AgentState) -> AgentState:

    raw_requirement = state["raw_requirement"]

    prompt = f"""
You are a senior business analyst and software engineer.

Convert the following raw user requirement into a structured
software development requirement.

RAW REQUIREMENT:

{raw_requirement}

Return ONLY valid JSON.

Use exactly this structure:

{{
    "summary": "short Jira ticket summary",
    "description": "clear detailed description of the requirement",
    "acceptance_criteria": [
        "criterion 1",
        "criterion 2"
    ],
    "technical_notes": [
        "technical consideration 1"
    ],
    "test_requirements": [
        "test requirement 1"
    ]
}}

Rules:

- Do not invent unrelated requirements.
- Keep the summary short and clear.
- Preserve the user's actual intent.
- Acceptance criteria must be testable.
- Technical notes should only contain useful implementation considerations.
- Test requirements should describe what should be tested.
- Do not return markdown.
- Do not return ```json.
"""

    response = await llm.ainvoke(prompt)

    content = response.content.strip()

    print(">>> STRUCTURE REQUIREMENT RESPONSE:")
    print(content)

    try:
        result = json.loads(content)

    except json.JSONDecodeError:

        print(">>> Failed to parse structured requirement JSON")

        result = {
            "summary": raw_requirement[:100],
            "description": raw_requirement,
            "acceptance_criteria": [],
            "technical_notes": [],
            "test_requirements": [],
        }

    return {
        **state,
        "summary": result.get(
            "summary",
            raw_requirement[:100]
        ),
        "description": result.get(
            "description",
            raw_requirement
        ),
        "acceptance_criteria": result.get(
            "acceptance_criteria",
            []
        ),
        "technical_notes": result.get(
            "technical_notes",
            []
        ),
        "test_requirements": result.get(
            "test_requirements",
            []
        ),
    }


# ============================================================
# STEP 2
# Analyze requirement and determine CREATE / MODIFY files
# ============================================================

async def analyze_requirement(state: AgentState) -> AgentState:

    print(">>> analyze_requirement START")

    repository_files = state.get(
        "repository_files",
        []
    )

    print(
        ">>> Repository files:",
        len(repository_files)
    )

    prompt = f"""
You are a senior software engineer analyzing a Jira requirement.

Requirement:

Summary:
{state.get("summary", "")}

Description:
{state.get("description", "")}

Acceptance Criteria:
{state.get("acceptance_criteria", [])}

Technical Notes:
{state.get("technical_notes", [])}

Test Requirements:
{state.get("test_requirements", [])}

Existing repository files:

{json.dumps(repository_files, indent=2)}

Your job is to determine which files are required to implement
the requirement.

IMPORTANT:

1. Existing files may be modified.
2. Required files that do not exist must be created.
3. Do NOT restrict your answer only to existing files.
4. If this is a new application or feature, generate the
   appropriate new file paths.
5. Do not invent unrelated files.
6. Use the existing repository structure when possible.
7. Do not create duplicate files if an appropriate existing
   file already exists.

Return ONLY valid JSON.

Use exactly this structure:

{{
    "analysis": "explanation of the implementation approach",

    "requirements": [
        "requirement 1",
        "requirement 2"
    ],

    "file_actions": [
        {{
            "file": "src/App.jsx",
            "action": "modify"
        }},
        {{
            "file": "src/components/Header.jsx",
            "action": "create"
        }}
    ]
}}

Allowed actions:

- create
- modify

Rules for CREATE:

Use "create" when the required file does not currently exist
in the repository.

Rules for MODIFY:

Use "modify" when the file already exists and needs changes.

Return ONLY JSON.
Do not return markdown.
Do not return ```json.
"""

    response = await llm.ainvoke(prompt)

    content = response.content.strip()

    print(">>> OLLAMA ANALYSIS RESPONSE:")
    print(content)

    try:
        result = json.loads(content)

    except json.JSONDecodeError:

        print(">>> Failed to parse analysis JSON")

        result = {
            "analysis": content,
            "requirements": [],
            "file_actions": [],
        }

    file_actions = result.get(
        "file_actions",
        []
    )

    # Validate file actions
    valid_actions = []

    existing_files = set(repository_files)

    for item in file_actions:

        file_path = item.get("file")
        action = item.get("action")

        if not file_path:
            continue

        if action not in ["create", "modify"]:
            continue

        # If AI says CREATE but file already exists,
        # convert it to MODIFY.
        if action == "create" and file_path in existing_files:

            action = "modify"

        # If AI says MODIFY but file does not exist,
        # convert it to CREATE.
        if action == "modify" and file_path not in existing_files:

            action = "create"

        valid_actions.append({
            "file": file_path,
            "action": action,
        })

    potential_files = [
        item["file"]
        for item in valid_actions
    ]

    print(">>> File actions:")
    print(json.dumps(valid_actions, indent=2))

    print(">>> Potential files:")
    print(potential_files)

    print(">>> analyze_requirement END")

    return {
        **state,
        "analysis": result.get(
            "analysis",
            ""
        ),
        "requirements": result.get(
            "requirements",
            []
        ),
        "potential_files": potential_files,
        "file_actions": valid_actions,
    }


# ============================================================
# STEP 3
# Read only EXISTING files
# ============================================================

async def read_source_files(state: AgentState) -> AgentState:

    print(">>> read_source_files START")

    selected_files = state.get(
        "potential_files",
        []
    )

    repository_files = set(
        state.get(
            "repository_files",
            []
        )
    )

    source_files = {}

    print(">>> Selected files:")
    print(selected_files)

    for file_path in selected_files:

        # ----------------------------------------------------
        # New file
        # ----------------------------------------------------

        if file_path not in repository_files:

            print(
                f">>> New file - no source to read: {file_path}"
            )

            continue

        # ----------------------------------------------------
        # Existing file
        # ----------------------------------------------------

        try:

            print(
                f">>> Reading existing file: {file_path}"
            )

            file_data = await get_file_content(
                file_path
            )

            source_files[file_path] = file_data[
                "content"
            ]

        except Exception as e:

            print(
                f">>> Failed to read {file_path}: {str(e)}"
            )

            source_files[file_path] = (
                f"Unable to read file: {str(e)}"
            )

    print(
        ">>> Source files loaded:",
        list(source_files.keys())
    )

    print(">>> read_source_files END")

    return {
        **state,
        "source_files": source_files,
    }


# ============================================================
# STEP 4
# Generate CREATE / MODIFY code changes
# ============================================================
async def generate_code_changes(
    state: AgentState
) -> AgentState:

    print(">>> generate_code_changes START")

    file_actions = state.get(
        "file_actions",
        []
    )

    source_files = state.get(
        "source_files",
        {}
    )

    repository_files = state.get(
        "repository_files",
        []
    )

    print(">>> File actions:")
    print(
        json.dumps(
            file_actions,
            indent=2
        )
    )

    print(">>> Existing source files:")
    print(
        list(source_files.keys())
    )

    # --------------------------------------------------------
    # Build source file information
    # --------------------------------------------------------

    source_text = ""

    for file_path, content in source_files.items():

        source_text += f"""

==============================
FILE: {file_path}
==============================

{content}

"""

    # --------------------------------------------------------
    # Build prompt
    # --------------------------------------------------------

    prompt = f"""
You are a senior software engineer.

Implement the following software requirement.

SUMMARY:
{state.get("summary", "")}

DESCRIPTION:
{state.get("description", "")}

ACCEPTANCE CRITERIA:
{json.dumps(
    state.get("acceptance_criteria", []),
    indent=2
)}

TECHNICAL NOTES:
{json.dumps(
    state.get("technical_notes", []),
    indent=2
)}

TEST REQUIREMENTS:
{json.dumps(
    state.get("test_requirements", []),
    indent=2
)}

EXISTING REPOSITORY FILES:
{json.dumps(
    repository_files,
    indent=2
)}

REQUIRED FILE ACTIONS:
{json.dumps(
    file_actions,
    indent=2
)}

EXISTING SOURCE CODE:
{source_text}


IMPORTANT RULES:

1. Implement ONLY the requested requirement.

2. For "create":
   Create the complete new file.

3. For "modify":
   Return the complete updated file.

4. Do not return partial source code.

5. Do not create unrelated files.

6. Do not change the technology stack unless explicitly
   required by the requirement.

7. Follow the existing project technology when possible.

8. If the repository is empty or only contains README.md,
   create the minimum files required by the requirement.

9. Do not create both .jsx and .tsx versions of the same file.

10. Use one consistent React approach.

11. If TypeScript is selected, use .tsx/.ts consistently.

12. If JavaScript is selected, use .jsx/.js consistently.

13. Do not invent unnecessary ESLint, Prettier or configuration
    files unless they are explicitly required.

14. Do not modify README.md unless it is actually required.

15. Every requested file must have complete valid content.

16. The "new_content" value must contain the entire file.

17. Do not use markdown code fences.

18. Do not add comments outside the JSON response.

19. Return ONLY valid JSON.

20. The first character of your response must be {{
   and the last character must be }}.


Return exactly this JSON structure:

{{
    "code_changes": [
        {{
            "file": "package.json",
            "action": "create",
            "reason": "Why this file is required",
            "changes": [
                "Specific change 1",
                "Specific change 2"
            ],
            "new_content": "COMPLETE FILE CONTENT"
        }}
    ]
}}
"""

    print(">>> Sending code generation request to Ollama...")

    response = await llm.ainvoke(prompt)

    content = response.content.strip()

    print(">>> OLLAMA RAW CODE GENERATION RESPONSE:")
    print(content)

    # --------------------------------------------------------
    # Remove accidental markdown code fences
    # --------------------------------------------------------

    if content.startswith("```"):

        print(
            ">>> Removing markdown code fences"
        )

        lines = content.splitlines()

        if lines:

            lines = lines[1:]

        if lines and lines[-1].strip() == "```":

            lines = lines[:-1]

        content = "\n".join(lines).strip()

    # --------------------------------------------------------
    # Try JSON parsing
    # --------------------------------------------------------

    try:

        result = json.loads(content)

    except json.JSONDecodeError as e:

        print(
            ">>> Failed to parse code generation JSON"
        )

        print(
            ">>> JSON ERROR:",
            str(e)
        )

        print(
            ">>> RAW CONTENT:"
        )

        print(content)

        # ----------------------------------------------------
        # Try to extract JSON object from response
        # ----------------------------------------------------

        try:

            start_index = content.find("{")
            end_index = content.rfind("}")

            if (
                start_index != -1
                and end_index != -1
                and end_index > start_index
            ):

                possible_json = content[
                    start_index:end_index + 1
                ]

                print(
                    ">>> Trying extracted JSON..."
                )

                result = json.loads(
                    possible_json
                )

                print(
                    ">>> Extracted JSON parsed successfully"
                )

            else:

                raise ValueError(
                    "No JSON object found in Ollama response."
                )

        except Exception as extraction_error:

            print(
                ">>> JSON extraction failed:"
            )

            print(
                str(extraction_error)
            )

            return {
                **state,
                "code_changes": [],
            }

    # --------------------------------------------------------
    # Validate response structure
    # --------------------------------------------------------

    if not isinstance(result, dict):

        print(
            ">>> Ollama response is not a JSON object"
        )

        return {
            **state,
            "code_changes": [],
        }

    raw_changes = result.get(
        "code_changes",
        []
    )

    if not isinstance(
        raw_changes,
        list
    ):

        print(
            ">>> code_changes is not a list"
        )

        return {
            **state,
            "code_changes": [],
        }

    # --------------------------------------------------------
    # Allowed files
    # --------------------------------------------------------

    allowed_files = {
        item.get("file")
        for item in file_actions
        if item.get("file")
    }

    print(
        ">>> Allowed files:"
    )

    print(
        allowed_files
    )

    # --------------------------------------------------------
    # Validate generated changes
    # --------------------------------------------------------

    validated_changes = []

    for change in raw_changes:

        if not isinstance(
            change,
            dict
        ):
            continue

        file_path = change.get(
            "file"
        )

        action = change.get(
            "action"
        )

        new_content = change.get(
            "new_content"
        )

        # ----------------------------------------------------
        # File validation
        # ----------------------------------------------------

        if not file_path:

            print(
                ">>> Ignoring change without file path"
            )

            continue

        if file_path not in allowed_files:

            print(
                f">>> Ignoring unauthorized file: "
                f"{file_path}"
            )

            continue

        # ----------------------------------------------------
        # Action validation
        # ----------------------------------------------------

        if action not in [
            "create",
            "modify",
        ]:

            print(
                f">>> Invalid action: "
                f"{action}"
            )

            continue

        # ----------------------------------------------------
        # Content validation
        # ----------------------------------------------------

        if new_content is None:

            print(
                f">>> Missing new_content: "
                f"{file_path}"
            )

            continue

        if not isinstance(
            new_content,
            str
        ):

            print(
                f">>> new_content is not string: "
                f"{file_path}"
            )

            continue

        # ----------------------------------------------------
        # Store validated change
        # ----------------------------------------------------

        validated_changes.append({
            "file": file_path,
            "action": action,
            "reason": change.get(
                "reason",
                ""
            ),
            "changes": change.get(
                "changes",
                []
            ),
            "new_content": new_content,
        })

    # --------------------------------------------------------
    # Print final result
    # --------------------------------------------------------

    print(
        ">>> Validated code changes:",
        len(validated_changes)
    )

    for change in validated_changes:

        print(
            f">>> {change['action'].upper()}: "
            f"{change['file']}"
        )

    print(
        ">>> generate_code_changes END"
    )

    return {
        **state,
        "code_changes": validated_changes,
    }