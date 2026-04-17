---
name: email-reply
description: "Draft a casual email reply. Use when user says 'reply to this email', 'draft a response', 'help me reply', or pastes an email they received and wants a response."
allowed-tools: ["Read"]
---

# Email Reply Drafter

Write a reply that sounds like the user, not like AI.

## Style

- Casual and direct
- Short paragraphs (1-2 sentences each)
- No corporate filler ("I hope this email finds you well", "Please don't hesitate to reach out")
- Match the formality level of the email you're replying to
- Default to friendly and concise

## Workflow

1. Read the email the user provides (pasted or from a file)

2. Ask two quick questions:
   - "What's the main thing you want to say back?"
   - "Any tone notes?" (e.g., "be extra nice", "keep it short", "be direct")

3. Draft the reply. Keep it under 8 lines unless the topic requires more.

4. Present the draft. Ask: "Want me to adjust anything?"

5. When approved, copy to clipboard if possible:
   ```bash
   echo "reply text" | pbcopy
   ```

## What NOT to do

- Don't add a subject line unless asked
- Don't add greetings like "Dear [Name]" -- just start with "Hey [first name],"
- Don't sign off with anything formal -- "Thanks!" or just the user's name is fine
