function FileList({ files, onFileSelect, selectedFile }) {
  if (!files?.length) {
    return <p>No files found.</p>;
  }

  return (
    <div style={{ marginTop: "20px" }}>
      <h3>Repository Files</h3>

      <ul>
        {files.map((file) => (
          <li key={file}>
            <button
              onClick={() => onFileSelect(file)}
              style={{
                border: "none",
                background: "none",
                cursor: "pointer",
                padding: "5px",
                fontWeight:
                  selectedFile === file ? "bold" : "normal",
              }}
            >
              {file}
            </button>
          </li>
        ))}
      </ul>
    </div>
  );
}

export default FileList;