import { useState } from "react";
import { motion } from "framer-motion";

export default function JiraCodeReviewApproval({
  issueKey,
  onApprove,
  loading = false,
}) {
  const [approved, setApproved] = useState(false);

  const handleApprove = async () => {
    setApproved(true);
    await onApprove();
  };

  return (
    <motion.div
      initial={{ opacity: 0, y: 10 }}
      animate={{ opacity: 1, y: 0 }}
      className="rounded-xl border border-gray-200 bg-white p-6 shadow-sm"
    >
      <h3 className="text-lg font-semibold text-gray-900">
        Pull Request Created
      </h3>

      <p className="mt-2 text-sm text-gray-600">
        Pull Request has been created successfully.
      </p>

      <div className="mt-4 rounded-lg bg-gray-50 p-4">
        <p className="text-sm text-gray-700">
          Do you want to move Jira ticket{" "}
          <span className="font-semibold">
            {issueKey}
          </span>{" "}
          to <strong>Code Review</strong>?
        </p>
      </div>

      <div className="mt-5 flex gap-3">
        <button
          onClick={handleApprove}
          disabled={loading || approved}
          className="rounded-lg bg-blue-600 px-5 py-2.5 text-sm font-medium text-white hover:bg-blue-700 disabled:cursor-not-allowed disabled:opacity-50"
        >
          {loading
            ? "Moving..."
            : "Yes, Move to Code Review"}
        </button>

        <button
          disabled={loading}
          className="rounded-lg border border-gray-300 px-5 py-2.5 text-sm font-medium text-gray-700 hover:bg-gray-50 disabled:opacity-50"
        >
          No, Keep Current Status
        </button>
      </div>
    </motion.div>
  );
}