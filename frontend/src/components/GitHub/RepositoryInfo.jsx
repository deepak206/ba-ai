function RepositoryInfo({ repository }) {
    if (!repository) {
      return null;
    }
  
    return (
      <div style={{ marginTop: "30px" }}>
        <h2>GitHub Repository</h2>
  
        <p>
          <strong>Repository:</strong> {repository.repository}
        </p>
  
        <p>
          <strong>Branch:</strong> {repository.branch}
        </p>
  
        <p>
          <strong>Files:</strong> {repository.files.length}
        </p>
      </div>
    );
  }
  
  export default RepositoryInfo;