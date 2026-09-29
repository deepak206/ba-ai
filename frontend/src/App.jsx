import { useState } from "react";
import { AnimatePresence, motion } from "framer-motion";

import WorkflowSteps from "./components/Workflow/WorkflowSteps";
import RequirementForm from "./components/Requirement/RequirementForm";

import JiraTicketCreated from "./components/Jira/JiraTicketCreated";
import JiraStatusApproval from "./components/Jira/JiraStatusApproval";

import BranchApproval from "./components/GitHub/BranchApproval";
import CodeAnalysis from "./components/AI/CodeAnalysis";
import CodeReview from "./components/AI/CodeReview";
import PullRequestApproval from "./components/GitHub/PullRequestApproval";
import JiraCodeReviewApproval from "./components/Jira/JiraCodeReviewApproval";

import {
  createJiraIssue,
  moveJiraIssueToInProgress,
  createFeatureBranch,
  analyzeCodeChanges,
  applyCodeChanges,
  createPullRequest,
  getRepositoryTree,
  moveJiraIssueToCodeReview
} from "./services/api";

function App() {
  const [jiraTicket, setJiraTicket] = useState(null);

  const [requirementLoading, setRequirementLoading] =
    useState(false);

  const [jiraStatusLoading, setJiraStatusLoading] =
    useState(false);

  const [developmentBranch, setDevelopmentBranch] =
    useState("");

  const [currentBranch, setCurrentBranch] =
    useState("");

  const [branchCreationLoading, setBranchCreationLoading] =
    useState(false);

  const [codeAnalysis, setCodeAnalysis] =
    useState(null);

  const [codeAnalysisLoading, setCodeAnalysisLoading] =
    useState(false);

  const [codeReviewLoading, setCodeReviewLoading] =
    useState(false);

  const [codeReviewFeedback, setCodeReviewFeedback] =
    useState("");

  const [codeReviewStatus, setCodeReviewStatus] =
    useState("pending");

  const [commitResult, setCommitResult] =
    useState(null);

  const [pullRequestLoading, setPullRequestLoading] =
    useState(false);

  const [pullRequestResult, setPullRequestResult] =
    useState(null);

  const [repository, setRepository] = useState(null);
  const [repositoryLoading, setRepositoryLoading] = useState(false);

  const [codeReviewApproval, setCodeReviewApproval] =
  useState(false);

  const [jiraCodeReviewResult, setJiraCodeReviewResult] =
    useState(null);

  /*
   * -----------------------------------------
   * STEP 1
   * Create Jira Ticket
   * -----------------------------------------
   */

  const handleRequirementSubmit = async (requirement) => {
    setRequirementLoading(true);

    try {
      const ticket = await createJiraIssue(requirement);

      setJiraTicket(ticket);

      return ticket;
    } finally {
      setRequirementLoading(false);
    }
  };

  /*
   * -----------------------------------------
   * STEP 2
   * Move Jira Ticket to In Progress
   * -----------------------------------------
   */

  const handleMoveJiraToInProgress = async (issueKey) => {
    setJiraStatusLoading(true);

    try {
      const result =
        await moveJiraIssueToInProgress(issueKey);

      setJiraTicket((current) => ({
        ...current,
        status: result.status,
      }));

      return result;
    } finally {
      setJiraStatusLoading(false);
    }
  };

  /*
   * -----------------------------------------
   * STEP 3
   * Create Feature Branch
   * -----------------------------------------
   */

  const handleCreateFeatureBranch = async (ticket) => {
    setBranchCreationLoading(true);
  
    try {
      const result = await createFeatureBranch({
        issueKey: ticket.key,
        summary: ticket.summary,
      });
  
      setDevelopmentBranch(result.branch);
      setCurrentBranch(result.branch);
  
      await handleLoadRepository();
  
      return result;
    } finally {
      setBranchCreationLoading(false);
    }
  };

  /*
   * -----------------------------------------
   * STEP 4
   * Analyze Code
   * -----------------------------------------
   */

  const handleAnalyzeCode = async () => {
    if (!jiraTicket) {
      throw new Error("Jira ticket is not available.");
    }

    if (!currentBranch) {
      throw new Error(
        "Development branch has not been created."
      );
    }

    setCodeAnalysisLoading(true);

    try {
      const result = await analyzeCodeChanges({
        issueKey: jiraTicket.key,
        summary: jiraTicket.summary,
        description: jiraTicket.description,

        acceptanceCriteria:
          jiraTicket.acceptance_criteria || [],

        technicalNotes:
          jiraTicket.technical_notes || [],

        testRequirements:
          jiraTicket.test_requirements || [],

        repositoryFiles: repository?.files || [],
      });

      setCodeAnalysis(result);

      return result;
    } finally {
      setCodeAnalysisLoading(false);
    }
  };

  /*
   * -----------------------------------------
   * STEP 5
   * Approve & Apply Code Changes
   * -----------------------------------------
   */

  const handleApproveCodeChanges = async () => {
    if (!codeAnalysis?.code_changes?.length) {
      return;
    }

    if (!currentBranch) {
      throw new Error(
        "Development branch has not been created."
      );
    }

    setCodeReviewLoading(true);

    try {
      const result = await applyCodeChanges({
        branch: currentBranch,
        issueKey: jiraTicket.key,
        changes: codeAnalysis.code_changes,
      });

      setCommitResult(result);
      setCodeReviewStatus("approved");

      return result;
    } finally {
      setCodeReviewLoading(false);
    }
  };

  /*
   * -----------------------------------------
   * STEP 6
   * Request Code Changes
   * -----------------------------------------
   */

  const handleRequestCodeChanges = async (feedback) => {
    setCodeReviewFeedback(feedback);
    setCodeReviewStatus("changes_requested");
  };

  /*
   * -----------------------------------------
   * STEP 7
   * Create Pull Request
   * -----------------------------------------
   */

  const handleCreatePullRequest = async () => {
    if (!jiraTicket) {
      throw new Error(
        "Jira ticket is not available."
      );
    }

    if (!currentBranch) {
      throw new Error(
        "Development branch is not available."
      );
    }

    if (!commitResult?.commit_sha) {
      throw new Error(
        "No committed changes are available."
      );
    }

    setPullRequestLoading(true);

    try {
      const result = await createPullRequest({
        issueKey: jiraTicket.key,
        summary: jiraTicket.summary,
        description: jiraTicket.description,
        branch: currentBranch,
        commitSha: commitResult.commit_sha,
      });

      setPullRequestResult(result);

      return result;
    } finally {
      setPullRequestLoading(false);
    }
  };
  
  const handleLoadRepository = async () => {
    setRepositoryLoading(true);
  
    try {
      const result = await getRepositoryTree();
  
      setRepository(result);
  
      return result;
    } finally {
      setRepositoryLoading(false);
    }
  };

  /*
   * -----------------------------------------
   * Workflow Step Calculation
   * -----------------------------------------
   */

  const getCurrentStep = () => {
    if (pullRequestResult) return 7;

    if (commitResult) return 6;

    if (
      codeReviewStatus === "approved" &&
      commitResult
    ) {
      return 6;
    }

    if (codeAnalysis?.code_changes?.length) {
      return 5;
    }

    if (codeAnalysis) {
      return 4;
    }

    if (developmentBranch) {
      return 3;
    }

    if (jiraTicket?.status === "In Progress") {
      return 2;
    }

    if (jiraTicket) {
      return 1;
    }

    return 0;
  };

  const currentStep = getCurrentStep();

  /*
   * -----------------------------------------
   * Animation
   * -----------------------------------------
   */

  const stepAnimation = {
    initial: {
      opacity: 0,
      y: 20,
    },

    animate: {
      opacity: 1,
      y: 0,
    },

    exit: {
      opacity: 0,
      y: -20,
    },

    transition: {
      duration: 0.35,
      ease: "easeOut",
    },
  };

  const handleMoveToCodeReview = async () => {
    try {
      setCodeReviewLoading(true);
  
      const result =
        await moveJiraIssueToCodeReview(
          jiraTicket.key
        );
  
      setJiraCodeReviewResult(result);
      setCodeReviewApproval(false);
  
    } catch (error) {
      console.error(
        "CODE REVIEW STATUS ERROR:",
        error
      );
  
      alert(error.message);
    } finally {
      setCodeReviewLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-slate-950 text-slate-200">

      {/* HEADER */}

      <header className="border-b border-slate-800 bg-slate-900/80 backdrop-blur">
        <div className="mx-auto flex max-w-[1400px] items-center justify-between px-6 py-4">

          <div className="flex items-center gap-3">

            <motion.div
              initial={{ scale: 0.8, opacity: 0 }}
              animate={{ scale: 1, opacity: 1 }}
              transition={{ duration: 0.3 }}
              className="flex h-10 w-10 items-center justify-center rounded-xl bg-blue-600 text-lg shadow-lg shadow-blue-600/20"
            >
              ⚡
            </motion.div>

            <div>
              <h1 className="font-semibold text-white">
                AI Development Agent
              </h1>

              <p className="text-xs text-slate-500">
                Intelligent software development workflow
              </p>
            </div>

          </div>

          <div className="flex items-center gap-2 text-xs text-emerald-400">
            <motion.span
              animate={{
                opacity: [1, 0.4, 1],
              }}
              transition={{
                duration: 1.5,
                repeat: Infinity,
              }}
              className="h-2 w-2 rounded-full bg-emerald-400 shadow-lg shadow-emerald-400/50"
            />

            System Online
          </div>

        </div>
      </header>

      {/* MAIN */}

      <main className="mx-auto max-w-[1400px] px-6 py-8">

        {/* WORKFLOW STEPS */}

        <motion.div
          initial={{ opacity: 0, y: -10 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.4 }}
        >
          <WorkflowSteps
            currentStep={currentStep}
          />
        </motion.div>

        {/* WORKFLOW CONTENT */}

        <div className="mt-8">

          <AnimatePresence mode="wait">

            {/* STEP 0 - REQUIREMENT */}

            {!jiraTicket && (
              <motion.div
                key="requirement"
                {...stepAnimation}
              >
                <RequirementForm
                  onSubmit={handleRequirementSubmit}
                  loading={requirementLoading}
                />
              </motion.div>
            )}

            {/* STEP 1 - JIRA TICKET */}

            {jiraTicket && !jiraTicket.status?.includes("Progress") && (
              <motion.div
                key="jira"
                {...stepAnimation}
                className="space-y-5"
              >

                <JiraTicketCreated
                  ticket={jiraTicket}
                />

                <JiraStatusApproval
                  ticket={jiraTicket}
                  onMoveToInProgress={
                    handleMoveJiraToInProgress
                  }
                  loading={jiraStatusLoading}
                />

              </motion.div>
            )}

            {/* STEP 2 - BRANCH */}

            {jiraTicket?.status === "In Progress" &&
              !developmentBranch && (
                <motion.div
                  key="branch"
                  {...stepAnimation}
                >

                  <BranchApproval
                    ticket={jiraTicket}
                    onCreateBranch={
                      handleCreateFeatureBranch
                    }
                    loading={branchCreationLoading}
                  />

                </motion.div>
              )}

            {/* STEP 3 - AI ANALYSIS */}

            {developmentBranch && !codeAnalysis && (
              <motion.div
                key="analysis"
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, y: -20 }}
                transition={{ duration: 0.35 }}
              >
                <CodeAnalysis
                  result={codeAnalysis}
                  loading={
                    codeAnalysisLoading ||
                    repositoryLoading
                  }
                  onAnalyze={handleAnalyzeCode}
                />

                {repositoryLoading && (
                  <div className="mt-4 rounded-xl border border-blue-500/30 bg-blue-500/10 p-4 text-sm text-blue-300">
                    Loading GitHub repository files...
                  </div>
                )}

                {repository && (
                  <div className="mt-4 rounded-xl border border-slate-700 bg-slate-900 p-4">
                    <div className="text-sm text-slate-400">
                      Repository files loaded
                    </div>

                    <div className="mt-1 text-lg font-semibold text-white">
                      {repository.files?.length || 0} files
                    </div>
                  </div>
                )}
              </motion.div>
            )}

            {/* STEP 4 - CODE REVIEW */}

            {codeAnalysis?.code_changes?.length > 0 &&
              !commitResult && (
                <motion.div
                  key="review"
                  {...stepAnimation}
                >

                  <CodeReview
                    result={codeAnalysis}
                    onApprove={
                      handleApproveCodeChanges
                    }
                    onRequestChanges={
                      handleRequestCodeChanges
                    }
                    loading={codeReviewLoading}
                  />

                  {codeReviewStatus ===
                    "changes_requested" && (
                    <motion.div
                      initial={{
                        opacity: 0,
                        y: 10,
                      }}
                      animate={{
                        opacity: 1,
                        y: 0,
                      }}
                      className="mt-4 rounded-xl border border-orange-500/30 bg-orange-500/10 p-4 text-sm text-orange-300"
                    >
                      <div className="font-medium">
                        Changes requested
                      </div>

                      <div className="mt-1 text-orange-200/80">
                        {codeReviewFeedback}
                      </div>
                    </motion.div>
                  )}

                </motion.div>
              )}

            {/* STEP 5 - COMMIT */}

            {commitResult && !pullRequestResult && (
              <motion.div
                key="commit"
                {...stepAnimation}
                className="space-y-5"
              >

                <div className="rounded-xl border border-green-500/30 bg-green-500/10 p-6">

                  <div className="flex items-center gap-3">

                    <motion.div
                      initial={{ scale: 0 }}
                      animate={{ scale: 1 }}
                      className="flex h-10 w-10 items-center justify-center rounded-full bg-green-500 text-white"
                    >
                      ✓
                    </motion.div>

                    <div>
                      <h2 className="text-lg font-semibold text-green-300">
                        Changes Committed Successfully
                      </h2>

                      <p className="text-sm text-green-200/70">
                        The approved AI-generated changes
                        have been committed to GitHub.
                      </p>
                    </div>

                  </div>

                  <div className="mt-6 space-y-3 text-sm">

                    <div>
                      <span className="text-slate-400">
                        Branch:
                      </span>

                      <span className="ml-2 font-mono text-white">
                        {commitResult.branch}
                      </span>
                    </div>

                    <div>
                      <span className="text-slate-400">
                        Commit:
                      </span>

                      <span className="ml-2 font-mono text-white">
                        {commitResult.commit_sha}
                      </span>
                    </div>

                    <div>
                      <span className="text-slate-400">
                        Files changed:
                      </span>

                      <span className="ml-2 text-white">
                        {commitResult.files_changed?.length || 0}
                      </span>
                    </div>

                  </div>

                  {commitResult.commit_url && (
                    <a
                      href={commitResult.commit_url}
                      target="_blank"
                      rel="noreferrer"
                      className="mt-5 inline-block text-sm font-medium text-blue-400 hover:text-blue-300 hover:underline"
                    >
                      View commit on GitHub →
                    </a>
                  )}

                </div>

                {/* PR APPROVAL */}

                <PullRequestApproval
                  ticket={jiraTicket}
                  branch={currentBranch}
                  commit={commitResult}
                  onCreatePullRequest={
                    handleCreatePullRequest
                  }
                  loading={pullRequestLoading}
                />

              </motion.div>
            )}

            {/* STEP 6 - PR CREATED */}

            {pullRequestResult && (
              <motion.div
                key="pull-request"
                {...stepAnimation}
              >

                <div className="rounded-xl border border-purple-500/30 bg-purple-500/10 p-6">

                  <div className="flex items-center gap-3">

                    <motion.div
                      initial={{ scale: 0 }}
                      animate={{ scale: 1 }}
                      className="flex h-10 w-10 items-center justify-center rounded-full bg-purple-500 text-white"
                    >
                      ✓
                    </motion.div>

                    <div>
                      <h2 className="text-lg font-semibold text-purple-300">
                        Pull Request Created
                      </h2>

                      <p className="text-sm text-purple-200/70">
                        The development branch is now ready
                        for review.
                      </p>
                    </div>

                  </div>

                  <div className="mt-5 space-y-3 text-sm">

                    <div>
                      <span className="text-slate-400">
                        PR:
                      </span>

                      <span className="ml-2 font-semibold text-white">
                        #{pullRequestResult.pull_request_number}
                      </span>
                    </div>

                    <div>
                      <span className="text-slate-400">
                        Branch:
                      </span>

                      <span className="ml-2 font-mono text-white">
                        {pullRequestResult.branch}
                      </span>
                    </div>

                    <div>
                      <span className="text-slate-400">
                        Target:
                      </span>

                      <span className="ml-2 font-mono text-white">
                        {pullRequestResult.base_branch}
                      </span>
                    </div>

                  </div>

                  {pullRequestResult.pull_request_url && (
                    <a
                      href={
                        pullRequestResult.pull_request_url
                      }
                      target="_blank"
                      rel="noreferrer"
                      className="mt-5 inline-block rounded-lg bg-purple-600 px-4 py-2 text-sm font-medium text-white transition hover:bg-purple-500"
                    >
                      Open Pull Request →
                    </a>
                  )}

                </div>

                {pullRequestResult && !jiraCodeReviewResult && (
                  <JiraCodeReviewApproval
                    issueKey={jiraTicket.key}
                    loading={codeReviewLoading}
                    onApprove={handleMoveToCodeReview}
                  />
                )}
                {jiraCodeReviewResult && (
                  <div className="rounded-xl border border-green-200 bg-green-50 p-5">
                    <h3 className="font-semibold text-green-800">
                      Jira Ticket Moved to Code Review
                    </h3>

                    <p className="mt-2 text-sm text-green-700">
                      {jiraTicket.key} is now in Code Review.
                    </p>
                  </div>
                )}
              </motion.div>
            )}

          </AnimatePresence>

        </div>

      </main>

    </div>
  );
}

export default App;