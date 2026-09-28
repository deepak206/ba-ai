import { useState } from "react";
import { motion } from "framer-motion";

const PullRequestApproval = ({
  ticket,
  branch,
  commit,
  onCreatePullRequest,
  loading = false,
}) => {
  const [created, setCreated] = useState(false);
  const [pullRequest, setPullRequest] = useState(null);
  const [error, setError] = useState("");

  if (!ticket || !branch || !commit) {
    return null;
  }

  const handleCreatePullRequest = async () => {
    setError("");

    try {
      const result = await onCreatePullRequest();

      setPullRequest(result);
      setCreated(true);
    } catch (err) {
      setError(
        err.message ||
          "Unable to create Pull Request"
      );
    }
  };

  if (created && pullRequest) {
    return (
      <motion.div
        initial={{
          opacity: 0,
          y: 10,
        }}
        animate={{
          opacity: 1,
          y: 0,
        }}
        className="rounded-xl border border-green-200 bg-green-50 p-6"
      >
        <h2 className="text-lg font-semibold text-green-800">
          Pull Request Created
        </h2>

        <div className="mt-4 space-y-2 text-sm">
          <div>
            <span className="font-medium">
              PR:
            </span>{" "}
            #{pullRequest.number}
          </div>

          <div>
            <span className="font-medium">
              Branch:
            </span>{" "}
            <span className="font-mono">
              {pullRequest.branch}
            </span>
          </div>

          <div>
            <span className="font-medium">
              Target:
            </span>{" "}
            <span className="font-mono">
              {pullRequest.base}
            </span>
          </div>
        </div>

        <a
          href={pullRequest.pull_request_url}
          target="_blank"
          rel="noreferrer"
          className="mt-5 inline-block rounded-lg bg-green-700 px-5 py-2.5 text-sm font-medium text-white hover:bg-green-800"
        >
          Open Pull Request →
        </a>
      </motion.div>
    );
  }

  return (
    <motion.div
      initial={{
        opacity: 0,
        y: 10,
      }}
      animate={{
        opacity: 1,
        y: 0,
      }}
      className="rounded-xl border border-gray-200 bg-white p-6 shadow-sm"
    >
      <h2 className="text-lg font-semibold text-gray-900">
        Create Pull Request
      </h2>

      <p className="mt-2 text-sm text-gray-600">
        The approved changes have been committed to:
      </p>

      <div className="mt-3 rounded-lg bg-gray-50 px-4 py-3 font-mono text-sm">
        {branch}
      </div>

      <p className="mt-4 text-sm text-gray-600">
        Would you like to raise a Pull Request from
        this branch to <strong>main</strong>?
      </p>

      {error && (
        <div className="mt-4 rounded-lg bg-red-50 p-3 text-sm text-red-700">
          {error}
        </div>
      )}

      <button
        type="button"
        onClick={handleCreatePullRequest}
        disabled={loading}
        className="mt-5 rounded-lg bg-gray-900 px-5 py-2.5 text-sm font-medium text-white hover:bg-gray-800 disabled:cursor-not-allowed disabled:opacity-50"
      >
        {loading
          ? "Creating Pull Request..."
          : "Raise Pull Request"}
      </button>
    </motion.div>
  );
};

export default PullRequestApproval;