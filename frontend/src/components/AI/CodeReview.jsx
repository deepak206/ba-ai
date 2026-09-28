import { useState } from "react";
import { motion } from "framer-motion";

const CodeReview = ({
  result,
  onApprove,
  onRequestChanges,
  loading = false,
}) => {
  const [feedback, setFeedback] = useState("");

  if (!result?.code_changes?.length) {
    return null;
  }

  const handleRequestChanges = async () => {
    if (!feedback.trim()) {
      return;
    }

    await onRequestChanges(feedback.trim());

    setFeedback("");
  };

  return (
    <motion.div
      initial={{ opacity: 0, y: 10 }}
      animate={{ opacity: 1, y: 0 }}
      className="space-y-5"
    >
      <div className="rounded-xl border border-yellow-200 bg-yellow-50 p-5">
        <h2 className="text-lg font-semibold text-gray-900">
          Human Code Review Required
        </h2>

        <p className="mt-2 text-sm text-gray-600">
          The AI has proposed changes. Review the changes
          before anything is written to GitHub.
        </p>
      </div>

      {result.code_changes.map((change, index) => (
        <div
          key={`${change.file}-${index}`}
          className="overflow-hidden rounded-xl border border-gray-200 bg-white shadow-sm"
        >
          {/* Header */}

          <div className="border-b border-gray-200 bg-gray-50 p-4">
            <div className="font-mono text-sm font-semibold text-gray-900">
              {change.file}
            </div>

            <p className="mt-2 text-sm text-gray-600">
              {change.reason}
            </p>
          </div>

          {/* Change summary */}

          <div className="border-b border-gray-200 p-4">
            <h3 className="text-sm font-semibold text-gray-900">
              Proposed Changes
            </h3>

            <ul className="mt-2 list-disc space-y-1 pl-5 text-sm text-gray-600">
              {change.changes?.map(
                (item, itemIndex) => (
                  <li key={itemIndex}>
                    {item}
                  </li>
                )
              )}
            </ul>
          </div>

          {/* Original */}

          <div className="p-4">
            <h3 className="mb-2 text-sm font-semibold text-gray-900">
              Original Code
            </h3>

            <pre className="max-h-[500px] overflow-auto rounded-lg bg-gray-950 p-4 text-xs leading-5 text-gray-200">
              <code>
                {result.source_files?.[change.file] ||
                  "Original source code unavailable."}
              </code>
            </pre>
          </div>

          {/* Proposed */}

          <div className="p-4">
            <h3 className="mb-2 text-sm font-semibold text-gray-900">
              Proposed Code
            </h3>

            <pre className="max-h-[500px] overflow-auto rounded-lg bg-gray-950 p-4 text-xs leading-5 text-gray-200">
              <code>
                {change.new_content}
              </code>
            </pre>
          </div>
        </div>
      ))}

      {/* Review Actions */}

      <div className="rounded-xl border border-gray-200 bg-white p-6 shadow-sm">
        <h3 className="text-lg font-semibold text-gray-900">
          Review Decision
        </h3>

        <div className="mt-4">
          <label className="text-sm font-medium text-gray-700">
            Feedback for AI
          </label>

          <textarea
            value={feedback}
            onChange={(event) =>
              setFeedback(event.target.value)
            }
            rows={4}
            placeholder="Example: The validation should happen on blur instead of submit."
            className="mt-2 w-full rounded-lg border border-gray-300 px-4 py-3 text-sm outline-none focus:border-gray-500"
          />
        </div>

        <div className="mt-5 flex flex-wrap gap-3">
          <button
            type="button"
            onClick={onApprove}
            disabled={loading}
            className="rounded-lg bg-green-600 px-5 py-2.5 text-sm font-medium text-white hover:bg-green-700 disabled:cursor-not-allowed disabled:opacity-50"
          >
            {loading
              ? "Processing..."
              : "Approve Changes"}
          </button>

          <button
            type="button"
            onClick={handleRequestChanges}
            disabled={
              loading || !feedback.trim()
            }
            className="rounded-lg border border-gray-300 bg-white px-5 py-2.5 text-sm font-medium text-gray-700 hover:bg-gray-50 disabled:cursor-not-allowed disabled:opacity-50"
          >
            Request Changes
          </button>
        </div>
      </div>
    </motion.div>
  );
};

export default CodeReview;