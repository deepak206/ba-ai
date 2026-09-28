function JiraTicket({ issue }) {
  if (!issue) {
    return null;
  }

  return (
    <div style={{ marginTop: "30px" }}>
      <h2>{issue.key}</h2>

      <p>
        <strong>Summary:</strong>
        <br />
        {issue.summary}
      </p>

      <p>
        <strong>Status:</strong>
        <br />
        {issue.status}
      </p>

      <p>
        <strong>Description:</strong>
        <br />
        {issue.description || "No description"}
      </p>
    </div>
  );
}

export default JiraTicket;
