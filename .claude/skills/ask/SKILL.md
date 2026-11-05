---
name: ask
description: Answer a question from Pranay's own vault — what he has already learned — citing notes, and showing gaps. Use when he says "/ask", "what do I know about", or "what have I learned about".
argument-hint: <question>
---

# /ask

Question: $ARGUMENTS

1. Search `notes/`, `maps/`, and `sources/` (grep for terms and cross-field synonyms; read the
   relevant notes and follow their links one or two hops).
2. Answer in two clearly separated parts:
   - **From your vault** — synthesize what his notes say, citing every claim with `[[Note]]`.
     Point out connections between the cited notes that bear on the question.
   - **Not in your vault yet** — briefly, what's missing or what general knowledge would add
     (clearly labeled as not from his notes).
3. Offer to `/learn` any gap he wants to keep. Don't write any notes unless he says yes.
