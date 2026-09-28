import { motion } from "framer-motion";
import StatusBadge from "../common/StatusBadge";

function JiraTicket({ issue }) {
  if (!issue) {
    return null;
  }

  return (
    <motion.div
      initial={{ opacity: 0, y: 15 }}
      animate={{ opacity: 1, y: 0 }}
      className="rounded-2xl border border-slate-800 bg-slate-900 p-6 shadow-xl shadow-black/10"
    >
      <div className="mb-5 flex items-center justify-between">
        <div>
          <p className="text-xs font-medium uppercase tracking-wider text-blue-400">
            Jira Ticket
          </p>

          <h2 className="mt-1 text-xl font-semibold text-white">
            {issue.key}
          </h2>
        </div>

        <StatusBadge status={issue.status} />
      </div>

      <h3 className="mb-3 text-lg font-medium text-slate-200">
        {issue.summary}
      </h3>

      <div className="rounded-xl bg-slate-950 p-4">
        <p className="mb-2 text-xs uppercase tracking-wide text-slate-500">
          Description
        </p>

        <p className="text-sm leading-6 text-slate-400">
          {issue.description || "No description"}
        </p>
      </div>
    </motion.div>
  );
}

export default JiraTicket;