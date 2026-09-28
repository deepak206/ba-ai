import { motion } from "framer-motion";

const steps = [
  "Jira",
  "Repository",
  "Branch",
  "Source Code",
  "AI Analysis",
  "Code Change",
  "Testing",
  "DEV",
  "UAT",
  "PROD",
];

function WorkflowSteps({ currentStep = 0 }) {
  return (
    <div className="mb-8 overflow-x-auto">
      <div className="flex min-w-max items-center">
        {steps.map((step, index) => {
          const completed = index < currentStep;
          const active = index === currentStep;

          return (
            <div
              key={step}
              className="flex items-center"
            >
              <motion.div
                initial={{ scale: 0.8, opacity: 0 }}
                animate={{ scale: 1, opacity: 1 }}
                transition={{
                  delay: index * 0.05,
                }}
                className="flex items-center gap-2"
              >
                <div
                  className={`
                    flex h-8 w-8 items-center justify-center
                    rounded-full text-xs font-semibold
                    ${
                      completed
                        ? "bg-emerald-500 text-white"
                        : active
                        ? "bg-blue-600 text-white shadow-lg shadow-blue-500/30"
                        : "bg-slate-800 text-slate-500"
                    }
                  `}
                >
                  {completed ? "✓" : index + 1}
                </div>

                <span
                  className={`
                    text-xs
                    ${
                      active
                        ? "font-semibold text-white"
                        : "text-slate-500"
                    }
                  `}
                >
                  {step}
                </span>
              </motion.div>

              {index < steps.length - 1 && (
                <div className="mx-3 h-px w-8 bg-slate-800" />
              )}
            </div>
          );
        })}
      </div>
    </div>
  );
}

export default WorkflowSteps;