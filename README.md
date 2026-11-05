# Learning vault

An [Obsidian](https://obsidian.md) vault that turns rough notes into a linked knowledge base.

Jot down whatever you learn, unstructured, in one place. When you run `learn`, the new text
is handed to [Claude Code](https://claude.com/claude-code) in the background. It splits the text
into atomic notes (one idea per note), links them to your existing notes with a stated reason for
each link (including cross-field connections), and writes a summary to `What's new.md`. You get a
Mac notification when it's done.


## How it works

1. **You write** in either of these places:
   - an Apple Note titled exactly **`Learning Log`** (easiest, and syncs from your iPhone), or
   - `Learning Log.md` in the vault root (fallback).

   Just keep appending. Never delete or reorganize old text; the script only looks at what's new.
2. **You run `learn`.** The script (`scripts/process_log.py`):
   - reads the Apple Note (via AppleScript) and `Learning Log.md`,
   - diffs each against a saved snapshot in `meta/` to find the new text,
   - runs `claude -p` headlessly in the vault, following the rules in `CLAUDE.md` and
     `.claude/skills/learn/SKILL.md`,
   - rebuilds the field maps (`maps/Biology.md`, `maps/Home.md`, ...) from the note tags,
   - sends a desktop notification.

   The snapshot is only updated if Claude succeeds, so if a run fails nothing is lost. Run
   `learn` again.
3. **You read** the results in Obsidian. Start at `What's new.md` or `maps/Home.md`.


## Folder layout

| Path | What it is |
|---|---|
| `CLAUDE.md` | House rules Claude follows: note format, link relations, domains |
| `.claude/skills/` | `learn`, `connect`, `ask` skills, also usable in an interactive Claude Code chat |
| `scripts/process_log.py` | The processor behind `learn` |
| `notes/` | Atomic notes (generated) |
| `sources/` | One note per book, paper, lecture, etc. (generated) |
| `maps/` | Field maps (auto-rebuilt) and theme maps |
| `meta/` | Snapshots, lock file, run log (`meta/processor.log`) |
| `templates/` | Note template |

## Setup (macOS)

**Requirements:** macOS (it uses Apple Notes and `osascript` notifications), Python 3.9+ (the
built-in `/usr/bin/python3` works; there are no dependencies), and Obsidian (optional, but it's
how you browse the notes).

1. **Install Claude Code and log in.**
   ```bash
   curl -fsSL https://claude.ai/install.sh | bash
   claude   # log in once, then exit
   ```
   The script expects the binary at **`~/.local/bin/claude`**, which is where the installer puts
   it. If yours is somewhere else (`which claude`), edit the `CLAUDE = ...` line near the top of
   `scripts/process_log.py`.

2. **Clone the repo.** It can live anywhere. The script finds the vault relative to its own
   location.
   ```bash
   git clone https://github.com/<you>/<repo>.git ~/Learning
   ```

3. **Add the `learn` command** to your shell config (`~/.zshrc`). Point it at wherever you cloned
   the repo:
   ```bash
   echo 'alias learn="/usr/bin/python3 ~/Learning/scripts/process_log.py"' >> ~/.zshrc
   source ~/.zshrc
   ```

4. **Create the Apple Note.** In Notes, make a note whose title (first line) is exactly
   `Learning Log`. Or skip this and just use `Learning Log.md` in the vault.

5. **First run:** type something in the log and run `learn`. macOS will ask to let your terminal
   control **Notes** (to read the log) and to show notifications. Allow both. If you missed the
   prompt, turn it on under System Settings → Privacy & Security → Automation.

6. **Open the folder in Obsidian** as a vault (Open folder as vault → pick the repo folder).

## Commands

| Command | What it does |
|---|---|
| `learn` | Process new text in the log (runs in the background) |
| `python3 scripts/process_log.py --maps` | Rebuild the field maps without processing anything |

In an interactive `claude` session inside the vault, you can also use `/learn <text>`,
`/connect [topic]` (look for new links) and `/ask <question>` (answer from your own notes).

## Customizing

- **Rules:** edit `CLAUDE.md` to change the note format, domains/tags or link vocabulary.
- **Personal references:** `CLAUDE.md`, the skills and the prompt in `process_log.py` refer to the
  original owner by name and background. Change these to describe you.
- **Troubleshooting:** check `meta/processor.log`, which records each run's Claude output and
  errors.
