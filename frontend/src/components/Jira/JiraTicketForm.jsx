function JiraTicketForm({
  issueKey,
  setIssueKey,
  onReadJira,
  loading,
}) {
  return (
    <div style={{ marginTop: "30px" }}>
      <input
        type="text"
        placeholder="Enter Jira Ticket ID"
        value={issueKey}
        onChange={(e) => setIssueKey(e.target.value)}
        style={{
          padding: "10px",
          width: "300px",
          marginRight: "10px",
        }}
      />

      <button
        onClick={onReadJira}
        disabled={loading}
      >
        {loading ? "Reading..." : "Read Jira"}
      </button>
    </div>
  );
}

export default JiraTicketForm;
