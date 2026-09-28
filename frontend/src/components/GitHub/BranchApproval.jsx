import { useState } from "react";
import { motion } from "framer-motion";

const BranchApproval = ({
  ticket,
  onCreateBranch,
  loading = false,
}) => {
  const [branchCreated, setBranchCreated] = useState(false);
  const [branchName, setBranchName] = useState("");
  const [error, setError] = useState("");

  if (!ticket) {
    return null;
  }

  const handleCreateBranch = async () => {
    setError("");

    try {
      const result = await onCreateBranch(ticket);

      setBranchName(result.branch);
      setBranchCreated(true);
    } catch (err) {
      setError(err.message || "Unable to create branch");
    }
  };

  if (branchCreated) {
    return (
      <motion.div
        initial={{ opacity: 0, y: 10 }}
        animate={{ opacity: 1, y: 0 }}
        className="rounded-xl border border-green-200 bg-green-50 p-5"
      >
        <div className="mb-2 text-sm font-semibold text-green-700">
          Development Branch Created
        </div>

        <div className="rounded-lg bg-white px-4 py-3 font-mono text-sm text-gray-800">
          {branchName}
        </div>

        <p className="mt-3 text-sm text-green-700">
          The branch was created from <strong>main</strong>.
        </p>
      </motion.div>
    );
  }

  return (
    <motion.div
      initial={{ opacity: 0, y: 10 }}
      animate={{ opacity: 1, y: 0 }}
      className="rounded-xl border border-gray-200 bg-white p-6 shadow-sm"
    >
      <h2 className="text-lg font-semibold text-gray-900">
        Create Development Branch
      </h2>

      <p className="mt-2 text-sm text-gray-600">
        Jira ticket{" "}
        <span className="font-semibold text-gray-900">
          {ticket.key}
        </span>{" "}
        is now In Progress.
      </p>

      <p className="mt-2 text-sm text-gray-600">
        Would you like to create a new development branch from{" "}
        <strong>main</strong>?
      </p>

      {error && (
        <div className="mt-4 rounded-lg bg-red-50 p-3 text-sm text-red-700">
          {error}
        </div>
      )}

      <div className="mt-5 flex gap-3">
        <button
          type="button"
          onClick={handleCreateBranch}
          disabled={loading}
          className="rounded-lg bg-gray-900 px-5 py-2.5 text-sm font-medium text-white transition hover:bg-gray-800 disabled:cursor-not-allowed disabled:opacity-50"
        >
          {loading
            ? "Creating Branch..."
            : "Create Branch from main"}
        </button>
      </div>
    </motion.div>
  );
};

export default BranchApproval;