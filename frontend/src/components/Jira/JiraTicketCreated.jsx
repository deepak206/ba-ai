import { motion } from "framer-motion";

function JiraTicketCreated({ ticket }) {
  if (!ticket) {
    return null;
  }

  const jiraUrl = ticket.self
    ? ticket.self.replace(
        "/rest/api/3/issue/",
        "/browse/"
      )
    : "#";

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      className="rounded-2xl border border-emerald-500/20 bg-slate-900 p-6 shadow-xl"
    >
      <div className="flex flex-col gap-4 sm:flex-row sm:items-start sm:justify-between">
        <div>
          <p className="text-xs uppercase tracking-wider text-emerald-400">
            Jira Ticket Created
          </p>

          <h2 className="mt-2 text-xl font-semibold text-white">
            {ticket.summary}
          </h2>

          <p className="mt-2 font-mono text-sm text-blue-400">
            {ticket.key}
          </p>
        </div>

        <span className="w-fit rounded-full bg-yellow-500/10 px-3 py-1 text-xs font-medium text-yellow-400">
          {ticket.status}
        </span>
      </div>

      <div className="mt-6 rounded-xl border border-slate-800 bg-slate-950 p-4">
        <p className="text-xs uppercase tracking-wider text-slate-500">
          Description
        </p>

        <p className="mt-2 whitespace-pre-wrap text-sm leading-6 text-slate-300">
          {ticket.description}
        </p>
      </div>

      <Section
        title="Acceptance Criteria"
        items={ticket.acceptance_criteria}
      />

      <Section
        title="Technical Notes"
        items={ticket.technical_notes}
      />

      <Section
        title="Test Requirements"
        items={ticket.test_requirements}
      />

      {jiraUrl !== "#" && (
        <div className="mt-6">
          <a
            href={jiraUrl}
            target="_blank"
            rel="noreferrer"
            className="inline-flex rounded-lg border border-slate-700 px-4 py-2 text-sm text-slate-300 transition hover:bg-slate-800"
          >
            Open in Jira ↗
          </a>
        </div>
      )}
    </motion.div>
  );
}


function Section({ title, items = [] }) {
  if (!items.length) {
    return null;
  }

  return (
    <div className="mt-5">
      <p className="mb-3 text-xs uppercase tracking-wider text-slate-500">
        {title}
      </p>

      <div className="space-y-2">
        {items.map((item, index) => (
          <div
            key={index}
            className="flex gap-3 rounded-lg border border-slate-800 bg-slate-950 p-3"
          >
            <span className="text-xs text-blue-400">
              {index + 1}.
            </span>

            <span className="text-sm text-slate-300">
              {item}
            </span>
          </div>
        ))}
      </div>
    </div>
  );
}


export default JiraTicketCreated;