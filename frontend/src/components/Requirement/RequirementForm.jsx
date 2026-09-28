import { useState } from "react";
import { motion } from "framer-motion";

function RequirementForm({
  onSubmit,
  loading = false,
}) {
  const [requirement, setRequirement] = useState("");
  const [error, setError] = useState("");

  const handleSubmit = async (event) => {
    event.preventDefault();

    const value = requirement.trim();

    if (!value) {
      setError("Please enter your requirement.");
      return;
    }

    setError("");

    try {
      await onSubmit(value);
    } catch (err) {
      setError(err.message);
    }
  };

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      className="rounded-2xl border border-slate-800 bg-slate-900 p-6 shadow-xl"
    >
      <div>
        <p className="text-xs uppercase tracking-wider text-blue-400">
          Requirement
        </p>

        <h1 className="mt-2 text-2xl font-semibold text-white">
          What would you like to build?
        </h1>

        <p className="mt-2 text-sm leading-6 text-slate-400">
          Describe the requirement in your own words.
          The AI Development Agent will create a Jira
          ticket from it.
        </p>
      </div>

      <form
        onSubmit={handleSubmit}
        className="mt-6"
      >
        <label className="mb-2 block text-sm font-medium text-slate-300">
          Raw Requirement
        </label>

        <textarea
          value={requirement}
          onChange={(event) =>
            setRequirement(event.target.value)
          }
          disabled={loading}
          rows={8}
          placeholder="Example:

Add email validation to the registration form.
If the user enters an invalid email address,
show a validation message and prevent submission."
          className="w-full resize-none rounded-xl border border-slate-800 bg-slate-950 p-4 text-sm leading-6 text-slate-300 outline-none placeholder:text-slate-600 focus:border-blue-500"
        />

        {error && (
          <motion.p
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            className="mt-2 text-sm text-red-400"
          >
            {error}
          </motion.p>
        )}

        <div className="mt-4 flex justify-end">
          <motion.button
            whileTap={{ scale: 0.97 }}
            type="submit"
            disabled={loading}
            className="flex items-center gap-2 rounded-lg bg-blue-600 px-6 py-3 text-sm font-medium text-white transition hover:bg-blue-500 disabled:cursor-not-allowed disabled:opacity-50"
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
              ? "Creating Jira Ticket..."
              : "Submit Requirement →"}
          </motion.button>
        </div>
      </form>
    </motion.div>
  );
}

export default RequirementForm;