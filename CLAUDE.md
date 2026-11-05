# Learning vault — house rules

This is Pranay's personal knowledge garden: an Obsidian vault of plain markdown files.
Pranay is a bioengineer / bioinformatician (PhD student) with deep interests in religion,
ecology, and anthropology. The purpose of this vault is to (1) **remember** what he learns and
(2) **see connections across fields** that he wouldn't make on his own.

**How it's used:** Pranay writes anything he learns, unstructured, in the Apple Note "Learning Log"
(Mac or iPhone). `Learning Log.md` in the vault also works as a fallback. Never edit either. When he
runs `learn` in a terminal (alias for `scripts/process_log.py`), new text is diffed against a
snapshot and handed to a background, headless Claude run. That run writes linked notes following
the rules below and reports in `What's new.md`; the script then rebuilds field maps and sends a
Mac notification. `learn` is the only thing he should ever have to run. Skills in `.claude/skills/`
(`learn`, `connect`, `ask`) are used internally or if he asks in chat.

## Layout

| Folder | Contents |
|---|---|
| `Learning Log.md` | The one file Pranay writes in. Never edit it. |
| `What's new.md` | Newest-first report of what each processing run did. |
| `notes/` | Atomic notes — **one idea per note**. The core of the vault. Flat, no subfolders. |
| `sources/` | One note per real source (book, lecture, podcast, paper, conversation, place visited). |
| `maps/` | Maps of Content: one per domain, plus theme maps. `maps/Home.md` is the entry point. |
| `meta/` | Bookkeeping (e.g. `rejected-connections.md`). Not knowledge. |
| `templates/` | Note template. |
| `scripts/` | `process_log.py` — the processor behind the `learn` command. |

## Notes

- **One idea per note.** If a capture contains three ideas, make three notes. A note about a
  whole topic ("Buddhism") is a map, not a note.
- **Title = the idea**, as a short phrase or claim, e.g. `Sacred groves as cultural niche construction`,
  `Niche construction`. Filename is the title + `.md`. Never use `: / \ ? * " < > | # ^ [ ]` in titles.
- **Before creating, check for an existing note on the same idea.** Extend it instead of making a
  near-duplicate.
- **Write for future-Pranay reading cold.** He is an expert in biology, not in theology or
  anthropological theory (and a theologian wouldn't know bioinformatics). Define jargon from the
  note's own field in plain words. Always include at least one concrete example.
- Keep the body short (roughly 100–300 words). Depth comes from links, not length.
- **Keep the source's claims separate from Pranay's own thinking.** His opinions, hunches, and reactions go
  under `## My take`, in his words as close as possible. Never invent opinions for him. Never
  rewrite or delete his words without asking.
- **Accuracy.** You may add well-established background context from your own knowledge, but:
  never fabricate citations, quotes, dates, or numbers; mark anything you're unsure of; put
  unresolved points under `## Open questions`. If his capture contains something that looks
  factually wrong, say so to him rather than silently copying or silently fixing it.

### Frontmatter (every note in `notes/`)

```yaml
---
created: 2026-11-04
tags: [ecology, anthropology]     # domains, from the list below
kind: concept                     # concept | claim | mechanism | example | person | question
source: "[[Pigs for the Ancestors]]"   # or plain text, or empty
confidence: medium                # how sure we are the content is right: high | medium | low
status: seedling                  # seedling | developing | solid
---
```

### Body structure

```markdown
# <Title>

**In one line:** <the idea in a single sentence>

## The idea
<plain-language explanation + a concrete example>

## Connections
- **<relation>** [[Other note]] — <why, one specific sentence>

## My take
<Pranay's own thoughts — only if he gave any>

## Open questions
- <things unresolved, to check, or to follow up>
```

Omit `My take` / `Open questions` if empty.

## Domains (used as tags)

`biology`, `bioinformatics`, `ecology`, `evolution`, `religion`, `anthropology`, `philosophy`,
`history`, `psychology`, `physics`, `chemistry`, `math-stats`, `computing`, `misc`.

Add a new domain only if notes clearly need it. When you do, add it to this list (its map is created automatically).

## Links — the most important part

Format, under `## Connections`:

```
- **analogous-to** [[Niche construction]] — both are feedback loops where the organism's own activity changes what it's selected for; differs in that ...
```

**Every link has a relation and a reason.** The reason must teach something: name the shared
mechanism or structure, or say exactly how one note bears on the other. Do not link notes just
because they share a topic. A bare `[[link]]` with no reason is a bug.

Relation vocabulary (use these; inverse in parentheses — **always add the inverse link to the
other note too**):

| Relation | Inverse |
|---|---|
| `analogous-to` — same structure, different domain | `analogous-to` |
| `same-phenomenon` — same thing studied under different names in different fields | `same-phenomenon` |
| `example-of` | `has-example` |
| `mechanism-for` / explains | `explained-by` |
| `builds-on` / requires | `prerequisite-for` |
| `extends` / refines | `extended-by` |
| `contrasts-with` — similar-looking but importantly different | `contrasts-with` |
| `contradicts` / in tension with | `contradicts` |

Rules for cross-domain links (the most valuable kind):
- Name the shared structure explicitly (feedback loop, signaling, boundary maintenance,
  selection, information transmission, exchange/reciprocity, ...).
- Say **where the analogy breaks**. A metaphor with no stated limit is a weak link.
- Prefer 2–5 strong links over 10 weak ones.

Inline `[[wikilinks]]` inside prose are fine too, but the `## Connections` list is the
authoritative record.

## Maps

- **Field maps** (`maps/Ecology.md`, etc.) and `maps/Home.md` are **rebuilt by a script** from note
  tags after every run. Never edit them; tagging a note correctly is enough.
- **Theme maps** (frontmatter `tags: [map, theme]`) are maintained by Claude. Create one when ≥3 notes
  from ≥2 fields share a cross-field idea (e.g. *Organisms shaping their own environment*). Open with
  a short **Synthesis** paragraph on what the notes share and where they disagree, then list notes
  with one-line reasons. Add new notes to fitting theme maps.

## Sources

Create `sources/<Title>.md` only for real sources Pranay engaged with. Contents: author/speaker,
year, type, a 2–3 line description, and a list of `[[notes]]` derived from it. Never invent a
source.

## Don'ts

- Don't create near-duplicate notes.
- Don't add links without reasons.
- Don't fabricate facts, citations, or Pranay's opinions.
- Don't run `git commit` unless asked (note: this folder sits inside a git repo rooted at `~`).
