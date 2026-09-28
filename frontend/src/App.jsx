import { useState } from "react";

import JiraTicketForm from "./components/Jira/JiraTicketForm";
import JiraTicket from "./components/Jira/JiraTicket";
import Loading from "./components/Jira/Loading";

import RepositoryInfo from "./components/GitHub/RepositoryInfo";
import FileList from "./components/GitHub/FileList";
import FileViewer from "./components/GitHub/FileViewer";

import { getJiraIssue, getRepositoryTree } from "./services/api";

function App() {
  const [issueKey, setIssueKey] = useState("");
  const [issue, setIssue] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const [repository, setRepository] = useState(null);
  const [githubLoading, setGithubLoading] = useState(false);
  const [githubError, setGithubError] = useState("");

  const [selectedFile, setSelectedFile] = useState("");
  const [fileContent, setFileContent] = useState(null);
  const [fileLoading, setFileLoading] = useState(false);
  const [fileError, setFileError] = useState("");

  const readJiraIssue = async () => {
    if (!issueKey.trim()) {
      setError("Please enter a Jira ticket ID");
      return;
    }

    setLoading(true);
    setError("");
    setIssue(null);

    try {
      const data = await getJiraIssue(issueKey);

      setIssue(data);
    } catch (error) {
      setError(error.message);
    } finally {
      setLoading(false);
    }
  };

  const readRepository = async () => {
    setGithubLoading(true);
    setGithubError("");
  
    try {
      const data = await getRepositoryTree();
      setRepository(data);
    } catch (error) {
      setGithubError(error.message);
    } finally {
      setGithubLoading(false);
    }
  };

  const readGithubFile = async (filePath) => {
    setSelectedFile(filePath);
    setFileContent(null);
    setFileError("");
    setFileLoading(true);
  
    try {
      const data = await getGithubFile(filePath);
  
      setFileContent(data);
    } catch (error) {
      setFileError(error.message);
    } finally {
      setFileLoading(false);
    }
  };

  return (
    <div style={{ maxWidth: "800px", margin: "50px auto" }}>
      <h1>AI Development Agent</h1>

      <JiraTicketForm
        issueKey={issueKey}
        setIssueKey={setIssueKey}
        onReadJira={readJiraIssue}
        loading={loading}
      />

      {loading && (
        <Loading message="Reading Jira ticket..." />
      )}

      {error && (
        <p style={{ color: "red" }}>
          {error}
        </p>
      )}

      <JiraTicket issue={issue} />

      <hr style={{ margin: "40px 0" }} />

      <button
        onClick={readRepository}
        disabled={githubLoading}
      >
        {githubLoading ? "Reading Repository..." : "Read GitHub Repository"}
      </button>

      {githubError && (
        <p style={{ color: "red" }}>
          {githubError}
        </p>
      )}

      <RepositoryInfo repository={repository} />

      {repository && (
        <FileList files={repository.files} />
      )}
      <FileList
        files={repository.files}
        onFileSelect={readGithubFile}
        selectedFile={selectedFile}
      />
      <FileViewer
        file={fileContent}
        loading={fileLoading}
        error={fileError}
      />
    </div>
  );
}

export default App;
