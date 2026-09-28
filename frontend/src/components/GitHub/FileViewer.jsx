function FileViewer({ file, loading, error }) {
    if (!file && !loading && !error) {
      return (
        <div style={{ marginTop: "30px" }}>
          <p>Select a file to view its source code.</p>
        </div>
      );
    }
  
    return (
      <div style={{ marginTop: "30px" }}>
        <h3>
          {file ? `File: ${file.path}` : "File"}
        </h3>
  
        {loading && <p>Loading file...</p>}
  
        {error && (
          <p style={{ color: "red" }}>
            {error}
          </p>
        )}
  
        {file && !loading && (
          <pre
            style={{
              background: "#f5f5f5",
              padding: "20px",
              overflowX: "auto",
              borderRadius: "5px",
            }}
          >
            <code>{file.content}</code>
          </pre>
        )}
      </div>
    );
  }
  
  export default FileViewer;