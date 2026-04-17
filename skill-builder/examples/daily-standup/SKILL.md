---
name: standup
description: "Draft a daily standup update. Use when user says 'standup', 'daily update', 'what did I do yesterday', or wants to write a quick status update for their team."
allowed-tools: ["Read", "Glob", "Grep", "Bash"]
---

# Daily Standup Drafter

Generate a short standup update based on recent work.

## Workflow

1. Check recent git activity:
   - Run `git log --oneline --since="yesterday" --author=$(git config user.name)` in the current repo
   - If no commits found, ask the user what they worked on

2. Ask the user:
   - "Anything to add to yesterday's work?"
   - "What are you focusing on today?"
   - "Any blockers?"

3. Format the update:
   ```
   **Yesterday:** [summary of work done]
   **Today:** [planned focus]
   **Blockers:** [blockers or "None"]
   ```

4. Keep it under 5 lines. No fluff.
