---
name: meeting-notes
description: "Process meeting notes into structured output. Use when user says 'process these notes', 'summarize this meeting', 'extract action items', or provides raw meeting notes or a transcript."
allowed-tools: ["Read", "Write", "Bash"]
---

# Meeting Notes Processor

Turn messy meeting notes or transcripts into structured, actionable output.

## Workflow

1. Get the notes -- either:
   - User pastes them directly
   - User provides a file path (read it)

2. Extract three sections:

   **Decisions Made**
   - What was decided and by whom
   - Only include actual decisions, not discussion points

   **Action Items**
   - Task, owner, and due date (if mentioned)
   - Format: `- [ ] [Task] -- [Owner] (due [date])`
   - If no owner was stated, flag it: `- [ ] [Task] -- [Owner TBD]`

   **Key Discussion Points**
   - Important context or debates that shaped the decisions
   - Keep to 3-5 bullets max -- not a transcript replay

3. Present the summary to the user

4. Ask: "Want me to save this to a file?" If yes, save to `meetings/YYYY-MM-DD-[topic].md`

## Tips

- If the notes are vague ("we talked about the project"), ask: "Can you clarify what was decided about [topic]?"
- Prefer action items over summaries -- meetings exist to produce next steps
- Skip anything that's just small talk or logistics ("let's schedule another meeting" is not an action item unless someone owns it)
