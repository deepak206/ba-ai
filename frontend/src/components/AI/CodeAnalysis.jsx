import { motion } from "framer-motion";

const CodeAnalysis = ({
  result,
  loading = false,
  onAnalyze,
}) => {
  if (loading) {
    return (
      <div className="rounded-xl border border-gray-200 bg-white p-6 shadow-sm">
        <div className="flex items-center gap-3">
          <div className="h-5 w-5 animate-spin rounded-full border-2 border-gray-300 border-t-gray-900" />

          <span className="text-sm text-gray-600">
            AI is analyzing the repository...
          </span>
        </div>
      </div>
    );
  }

  if (!result) {
    return (
      <div className="rounded-xl border border-gray-200 bg-white p-6 shadow-sm">
        <h2 className="text-lg font-semibold text-gray-900">
          AI Code Analysis
        </h2>

        <p className="mt-2 text-sm text-gray-600">
          Analyze the Jira requirement and generate proposed
          code changes.
        </p>

        <button
          type="button"
          onClick={onAnalyze}
          className="mt-5 rounded-lg bg-gray-900 px-5 py-2.5 text-sm font-medium text-white hover:bg-gray-800"
        >
          Analyze Code
        </button>
      </div>
    );
  }

  return (
    <motion.div
      initial={{ opacity: 0, y: 10 }}
      animate={{ opacity: 1, y: 0 }}
      className="space-y-5"
    >
      <div className="rounded-xl border border-gray-200 bg-white p-6 shadow-sm">
        <h2 className="text-lg font-semibold text-gray-900">
          AI Analysis
        </h2>

        <p className="mt-3 text-sm leading-6 text-gray-600">
          {result.analysis}
        </p>
      </div>

      <div className="rounded-xl border border-gray-200 bg-white p-6 shadow-sm">
        <h3 className="font-semibold text-gray-900">
          Relevant Files
        </h3>

        <div className="mt-3 space-y-2">
          {result.potential_files?.map((file) => (
            <div
              key={file}
              className="rounded-lg bg-gray-50 px-4 py-2 font-mono text-sm text-gray-700"
            >
              {file}
            </div>
          ))}
        </div>
      </div>

      <div className="rounded-xl border border-gray-200 bg-white p-6 shadow-sm">
        <h3 className="font-semibold text-gray-900">
          Proposed Code Changes
        </h3>

        <div className="mt-4 space-y-5">
          {result.code_changes?.map(
            (change, index) => (
              <div
                key={`${change.file}-${index}`}
                className="rounded-lg border border-gray-200"
              >
                <div className="border-b border-gray-200 bg-gray-50 px-4 py-3">
                  <div className="font-mono text-sm font-semibold text-gray-900">
                    {change.file}
                  </div>

                  <p className="mt-1 text-sm text-gray-600">
                    {change.reason}
                  </p>
                </div>

                <div className="p-4">
                  <h4 className="text-sm font-semibold text-gray-800">
                    Changes
                  </h4>

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
              </div>
            )
          )}
        </div>
      </div>
    </motion.div>
  );
};

export default CodeAnalysis;