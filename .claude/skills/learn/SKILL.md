---
name: learn
description: Capture something Pranay learned (a thought, quote, fact, paragraph, link, or messy notes) into atomic notes in the vault, linked with reasons to related existing notes. Use when he says "/learn", "log this", "I just learned", or pastes something to remember.
argument-hint: <what you learned, in any form>
---

# /learn

Input: $ARGUMENTS

Follow `CLAUDE.md` exactly. Steps:

1. **Understand the capture.** If it's a URL, fetch it. If it's ambiguous (you can't tell what the
   actual idea is, or what he thinks vs. what the source says), ask **one** short clarifying
   question. Otherwise don't ask — proceed.

2. **Split into ideas.** Identify the distinct ideas (usually 1–3). Each becomes its own note.
   Separate anything that is Pranay's own reaction/opinion → it goes in `## My take`.

3. **Search the vault for related material** before writing:
   - `ls notes/ maps/` to see all titles.
   - `grep -ril` across `notes/` for key terms **and their synonyms in other fields** (e.g. for
     "reciprocity" also try "gift", "mutualism", "exchange", "cooperation"; for "homeostasis" also
     "feedback", "regulation", "equilibrium"). Think about what this idea would be called in
     biology, ecology, religion, and anthropology.
   - Read the most promising candidates fully.
   - If a note on the **same idea** already exists → extend that note instead of creating a new one.

4. **Write the note(s)** in `notes/` using the frontmatter and body structure from `CLAUDE.md`.
   `created` = today.

5. **Link.** Add 1–5 links with relation + reason. For every link, add the inverse link
   (with its own reason) to the target note's `## Connections`. Look especially for one
   cross-domain link; if a genuinely good one exists, include it, but never force a weak one.

6. **Source.** If there's a real, identifiable source, create or update `sources/<Title>.md`
   and add the new note to its list.

7. **Maps.** Don't touch field maps or `maps/Home.md`: they're rebuilt from tags by a script. If the
   note fits an existing theme map, add it there. If ≥3 notes from ≥2 fields now share a theme with
   no map, create the theme map (`tags: [map, theme]`).

8. **Report back briefly:** notes created/updated (as `[[links]]`), each connection made in one
   line, and — if you spotted a possible connection you weren't confident enough to write — mention
   it as a question. Flag anything in his capture that looked factually off.
