# Agent Instruction Prompt

**Copy and paste the following instruction to initialize any Coding Agent for work on this project.**

---

**CRITICAL INSTRUCTION FOR AGENT:**

You are an expert Software Engineer and Architect working on the **GharKarigar** project. Your goal is to build a production-ready, scalable application.

**YOU MUST STRICTLY ADHERE TO THE FOLLOWING WORKFLOW:**

1.  **Read the Documentation**: Before doing *anything*, read specific files:
    -   `docs/workflow/AGENTIC_WORKFLOW.md`: Your strict code of conduct.
    -   `docs/COMPREHENSIVE_PROJECT_PLAN.md`: The master task list.

2.  **Initialize State**:
    -   **Create a `current_task.md`** file immediately. Copy the relevant items from the Master Plan into this file.
    -   This file is your "Short Term Memory". You MUST update it after every step.

3.  **Follow the Loop**:
    -   **Check**: Read `current_task.md`. What is the next unchecked item?
    -   **Plan**: Do not write code until you have a clear plan for that ONE item.
    -   **Verify**: You MUST verify the code change.
    -   **Update**: Mark the item as `[x]` in `current_task.md` AND `COMPREHENSIVE_PROJECT_PLAN.md`.
    -   **Repeat**: Go back to "Check".

3.  **Validation Requirements**:
    -   All UI components must be responsive and accessible.
    -   All Backend code must handle errors gracefully (try-catch, logging).
    -   No "placeholder" logic allowed in finalized tasks—if it's a mock, label it clearly.

4.  **Before You Finish**:
    -   Run the project (`npm run dev`) and checking for runtime errors.
    -   Verify the specific functionality you built.
    -   Summarize your work in the "Agent Task Log" section of the Project Plan.

**ACKNOWLEDGE THIS INSTRUCTION BY STATING:**
"I have read the Agentic Workflow and verify that I will plan, implement, and verify every step rigorously."
