# Agentic Development Workflow

This document outlines the strict workflow that all AI agents must follow when working on the **GharKarigar** project. This framework ensures high-quality, production-ready code through rigorous planning, verification, and iterative development.

## 1. Core Philosophy
*   **Think before you act.** Never rush into coding without a clear plan.
*   **Verify everything.** Code that isn't running or tested doesn't exist.
*   **Granularity is key.** Break tasks down into the smallest possible units of work.
*   **Documentation is code.** Keep task lists, plans, and architectural decisions up to date.

## 2. Workflow Stages

### Phase 1: Planning & Architecture (The Brain)
**Input:** User Request / Feature Idea
**Output:** Detailed Implementation Plan & Architecture Spec

1.  **Requirement Analysis**:
    *   Read all relevant documentation.
    *   Clarify ambiguities with the user.
    *   Identify dependencies (e.g., Database schema changes, API endpoints).
2.  **Solution Design**:
    *   **Architecture**: Define how new components fit into the existing system.
    *   **Schema**: Propose Prisma schema changes if needed.
    *   **UI/UX**: Describe the interface (or generate mockups).
3.  **Task Breakdown**:
    *   Create or update `docs/COMPREHENSIVE_PROJECT_PLAN.md`.
    *   Break the feature into granular steps (e.g., "Create API Route", "Create UI Component", "Add Validation").

### Phase 2: Setup & Environment
1.  **Context Loading**:
    *   Read existing related files (`read_file`).
    *   Understand the current state of variables, styles, and utilities.
2.  **Tool Check**:
    *   Ensure strict adherence to the technology stack (e.g., Tailwind CSS, Next.js, Prisma).

### Phase 3: The Execution Loop (The Hands)
**CRITICAL: You must maintain a `current_task.md` or `task.md` file.**

For *each* granular task in the plan:

1.  **Check Context**:
    *   Read `docs/workflow/AGENTIC_WORKFLOW.md` (Yes, again. Ensure you aren't skipping steps).
    *   Read your local `current_task.md` to see where you are.
2.  **Pre-Computation (Thinking)**:
    *   Draft the code change mentally or in a scratchpad.
    *   **Hypothesize**: "If I change X, Y should happen."
3.  **Implementation**:
    *   **Test-First (Recommended)**: Write a test case (unit, integration, or script) that fails.
    *   **Code**: specific, targeted changes. Avoid modifying unrelated files.
4.  **Verification (Self-Healing)**:
    *   **Run the Code**: Execute the dev server or script.
    *   **Validate**:
        *   Does the build pass? (`npm run build`).
        *   Do lint checks pass? (`npm run lint`).
        *   Does the feature work as expected? (Use browser tool or `curl`).
    *   **Heal**: If it fails, do NOT blindly retry. Analyze the error -> Adjust Plan -> Fix.
    *   **Automated Tests**: If a test suite exists, run it.
6.  **Loop Closure**:
    *   **Metacognition (Reflect)**: "Did this task actually achieve the user's granular goal?"
    *   **Context Engineering**: "Is my `task.md` clean? Do I need to summarize previous steps to save context window?"
    *   **Repeat**: Go back to "Check".

## 4. The "Am I Drifting?" Check (Metacognition)
Before every single tool call, ask yourself:
1.  "Is this step in my written plan?" -> If NO, stop and update the plan.
2.  "Have I verified the previous step?" -> If NO, verify it now.
3.  "Did I update the status file?" -> If NO, update it.
4.  "Do I have enough context to proceed?" -> If NO, read relevant files again.

## 5. Strict Rules for Agents
1.  **Never** submit code that hasn't been run/verified.
2.  **Never** make massive changes in one go. Steps must be incremental.
3.  **Always** check for existing reusable components before creating new ones.
4.  **Always** maintain the `current_task.md` state.
5.  **Always** loop back to this workflow.

## 4. Verification Checklists

### UI Changes
- [ ] Responsive check (Mobile/Desktop).
- [ ] Theme consistency (Dark/Light mode).
- [ ] No layout shifts.

### Backend Changes
- [ ] Schema validity (`npx prisma validate`).
- [ ] API Response types match Frontend expectations.
- [ ] Error handling (Try/Catch blocks present).
