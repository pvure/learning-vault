---
name: connect
description: Hunt for non-obvious connections between notes in the vault — especially across domains — and propose them for Pranay to accept or reject. Use when he says "/connect", "find connections", or "what links X and Y". Optional argument: a note title, domain, or theme to focus on.
argument-hint: [optional focus: note title, domain, or theme]
---

# /connect

Focus (may be empty): $ARGUMENTS

1. **Load the vault.** Read all of `notes/` (it's small enough; if it ever exceeds ~300 notes,
   read titles + `In one line` summaries first and then read candidates fully). Read
   `meta/rejected-connections.md` so you never re-propose a rejected pair.

2. **Find candidates.** If a focus was given, look for connections to/from it. Otherwise prioritize:
   - Pairs of notes in **different domains** that are **not yet linked** (directly or via one hop).
   - Notes with 0–1 connections (orphans).
   - Shared deep structures: feedback/regulation, signaling & honest signals, boundaries &
     membership, inheritance & transmission, exchange & reciprocity, sacrifice & cost,
     selection at multiple levels, information & meaning, scale transitions, purity/contamination,
     symbiosis, time & cycles.
   - Tensions: two notes that make incompatible claims.

3. **Quality bar.** Propose 3–6 connections. Each must:
   - name the relation (from the vocabulary in `CLAUDE.md`),
   - state the shared structure or the precise tension in 1–2 sentences,
   - state **where it breaks down**,
   - be something that would teach Pranay something — not "both are about nature".
   Surface-level similarities are worse than nothing; propose fewer if that's all there is.

4. **Present** them as a numbered list and ask which to accept (he can also edit the wording).
   Optionally, for the best one, pose a question he could think about ("If ritual is a regulator,
   what plays the role of the sensor?").

5. **Write accepted ones** into both notes' `## Connections` (relation + inverse, with reasons).
   Update/create theme maps if a theme emerges. Append rejected ones to
   `meta/rejected-connections.md` as `- [[A]] ↔ [[B]] (relation) — rejected YYYY-MM-DD: reason if given`.
