const API_BASE_URL = "http://127.0.0.1:8000";

/*
|--------------------------------------------------------------------------
| Jira
|--------------------------------------------------------------------------
*/

export const createJiraIssue = async (requirement) => {
  const response = await fetch(
    `${API_BASE_URL}/jira/create`,
    {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        requirement,
      }),
    }
  );

  if (!response.ok) {
    const error = await response.json().catch(() => null);

    throw new Error(
      error?.detail || "Unable to create Jira ticket"
    );
  }

  return response.json();
};


export const moveJiraIssueToInProgress = async (
  issueKey
) => {
  const response = await fetch(
    `${API_BASE_URL}/jira/${encodeURIComponent(
      issueKey
    )}/in-progress`,
    {
      method: "POST",
    }
  );

  if (!response.ok) {
    const error = await response.json().catch(
      () => null
    );

    throw new Error(
      error?.detail ||
        "Unable to move Jira ticket to In Progress"
    );
  }

  return response.json();
};


/*
|--------------------------------------------------------------------------
| GitHub
|--------------------------------------------------------------------------
*/

export const createFeatureBranch = async ({
  issueKey,
  summary,
}) => {
  const response = await fetch(
    `${API_BASE_URL}/github/feature-branch`,
    {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        issue_key: issueKey,
        summary,
      }),
    }
  );

  if (!response.ok) {
    const error = await response.json().catch(() => null);

    throw new Error(
      error?.detail ||
        "Unable to create development branch"
    );
  }

  return response.json();
};


export const applyCodeChanges = async ({
  branch,
  issueKey,
  changes,
}) => {
  const response = await fetch(
    `${API_BASE_URL}/github/apply-changes`,
    {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        branch,
        issue_key: issueKey,
        changes,
      }),
    }
  );

  if (!response.ok) {
    const error = await response.json().catch(
      () => null
    );

    throw new Error(
      error?.detail ||
        "Unable to apply code changes"
    );
  }

  return response.json();
};


export const createPullRequest = async ({
  issueKey,
  summary,
  description,
  branch,
  commitSha,
}) => {
  const response = await fetch(
    `${API_BASE_URL}/github/pull-request`,
    {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        issue_key: issueKey,
        summary,
        description,
        branch,
        commit_sha: commitSha,
      }),
    }
  );

  if (!response.ok) {
    const error = await response.json().catch(
      () => null
    );

    throw new Error(
      error?.detail ||
        "Unable to create Pull Request"
    );
  }

  return response.json();
};


/*
|--------------------------------------------------------------------------
| AI
|--------------------------------------------------------------------------
*/

export const analyzeCodeChanges = async ({
  issueKey,
  summary,
  description,
  acceptanceCriteria,
  technicalNotes,
  testRequirements,
  repositoryFiles,
}) => {
  const response = await fetch(
    `${API_BASE_URL}/ai/analyze-code`,
    {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        issue_key: issueKey,
        summary,
        description,
        acceptance_criteria: acceptanceCriteria,
        technical_notes: technicalNotes,
        test_requirements: testRequirements,
        repository_files: repositoryFiles,
      }),
    }
  );

  if (!response.ok) {
    const error = await response.json().catch(
      () => null
    );

    throw new Error(
      error?.detail ||
        "Unable to analyze code changes"
    );
  }

  return response.json();
};

export const getRepositoryTree = async () => {
    const response = await fetch(
      `${API_BASE_URL}/github/tree`
    );
  
    if (!response.ok) {
      const error = await response.json().catch(() => null);
  
      throw new Error(
        error?.detail ||
          "Unable to retrieve GitHub repository"
      );
    }
  
    return response.json();
  };