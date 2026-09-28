const API_BASE_URL = "http://127.0.0.1:8000";

export const getJiraIssue = async (issueKey) => {
  const response = await fetch(
    `${API_BASE_URL}/jira/${issueKey.trim()}`
  );

  if (!response.ok) {
    throw new Error("Unable to retrieve Jira ticket");
  }

  return response.json();
};

export const getRepositoryTree = async () => {
    const response = await fetch(
      `${API_BASE_URL}/github/tree`
    );
  
    if (!response.ok) {
      throw new Error("Unable to retrieve GitHub repository");
    }
  
    return response.json();
  };

  export const getGithubFile = async (path) => {
    const response = await fetch(
      `${API_BASE_URL}/github/file?path=${encodeURIComponent(path)}`
    );
  
    if (!response.ok) {
      throw new Error("Unable to retrieve GitHub file");
    }
  
    return response.json();
  };