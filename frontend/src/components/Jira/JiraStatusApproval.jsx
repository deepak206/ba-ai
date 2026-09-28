import { useState } from "react";
import { motion } from "framer-motion";

function JiraStatusApproval({
  ticket,
  onMoveToInProgress,
  loading = false,
}) {
  const [decision, setDecision] = useState(null);
  const [error, setError] = useState("");

  if (!ticket) {
    return null;
  }

  const handleMoveToProgress = async () => {
    setError("");

    try {
      const result = await onMoveToInProgress(
        ticket.key
      );

      setDecision(result);
    } catch (err) {
      setError(err.message);
    }
  };

  if (decision) {
    return (
      <motion.div
        initial={{ opacity: 0, y: 15 }}
        animate={{ opacity: 1, y: 0 }}
        className="rounded-2xl border border-blue-500/20 bg-slate-900 p-6"
      >
        <p className="text-xs uppercase tracking-wider text-blue-400">
          Jira Status Updated
        </p>

        <div className="mt-4 flex items-center gap-3">
          <span className="flex h-8 w-8 items-center justify-center rounded-full bg-blue-500/10 text-blue-400">
            ✓
          </span>

          <div>
            <p className="font-medium text-white">
              {ticket.key}
            </p>

            <p className="text-sm text-slate-400">
              Ticket is now In Progress.
            </p>
          </div>
        </div>
      </motion.div>
    );
  }

  return (
    <motion.div
      initial={{ opacity: 0, y: 15 }}
      animate={{ opacity: 1, y: 0 }}
      className="rounded-2xl border border-slate-800 bg-slate-900 p-6"
    >
      <p className="text-xs uppercase tracking-wider text-yellow-400">
        Action Required
      </p>

      <h2 className="mt-2 text-xl font-semibold text-white">
        Start Development?
      </h2>

      <p className="mt-2 text-sm leading-6 text-slate-400">
        Jira ticket{" "}
        <span className="font-mono text-blue-400">
          {ticket.key}
        </span>{" "}
        is currently{" "}
        <span className="text-yellow-400">
          {ticket.status}
        </span>
        .
      </p>

      <p className="mt-3 text-sm text-slate-300">
        Do you want to move this ticket to
        <span className="ml-1 font-medium text-blue-400">
          In Progress
        </span>
        ?
      </p>

      {error && (
        <div className="mt-4 rounded-lg border border-red-500/20 bg-red-500/10 p-3 text-sm text-red-400">
          {error}
        </div>
      )}

      <div className="mt-5 flex flex-wrap gap-3">
        <motion.button
          whileTap={{ scale: 0.97 }}
          onClick={handleMoveToProgress}
          disabled={loading}
          className="flex items-center gap-2 rounded-lg bg-blue-600 px-5 py-2.5 text-sm font-medium text-white hover:bg-blue-500 disabled:cursor-not-allowed disabled:opacity-50"
        >
          {loading && (
            <motion.span
              animate={{ rotate: 360 }}
              transition={{
                duration: 0.8,
                repeat: Infinity,
                ease: "linear",
              }}
              className="h-4 w-4 rounded-full border-2 border-white/30 border-t-white"
            />
          )}

          {loading
            ? "Updating..."
            : "Move to In Progress"}
        </motion.button>

        <button
          onClick={() => setDecision({
            status: "To Do",
          })}
          disabled={loading}
          className="rounded-lg border border-slate-700 px-5 py-2.5 text-sm text-slate-300 hover:bg-slate-800 disabled:opacity-50"
        >
          Keep as To Do
        </button>
      </div>
    </motion.div>
  );
}

export default JiraStatusApproval;