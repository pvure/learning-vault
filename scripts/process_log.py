#!/usr/bin/env python3
"""Process new text in "Learning Log.md" into linked notes. Run on demand with the `learn` command.

`learn` returns immediately; a detached worker hands the new text (diffed against a snapshot)
to Claude Code headlessly, rebuilds the domain maps from note tags, and sends a Mac
notification when done. The snapshot is updated only if Claude succeeds, so nothing is lost.

The log file itself is never modified. Python 3.9-compatible, stdlib only.
"""
import datetime as dt
import difflib
import fcntl
import os
import pathlib
import re
import subprocess
import sys

VAULT = pathlib.Path(__file__).resolve().parent.parent
LOG = VAULT / "Learning Log.md"
SNAPSHOT = VAULT / "meta" / ".log_snapshot.md"
NOTE_NAME = "Learning Log"  # Apple Notes note (main place to write; syncs from iPhone)
NOTE_SNAPSHOT = VAULT / "meta" / ".notes_snapshot.txt"
RUNLOG = VAULT / "meta" / "processor.log"
LOCK = VAULT / "meta" / ".lock"
CLAUDE = str(pathlib.Path.home() / ".local" / "bin" / "claude")

TOOLS = "Read Write Edit Glob Grep WebFetch WebSearch"


def log(msg):
    RUNLOG.parent.mkdir(exist_ok=True)
    with RUNLOG.open("a") as f:
        f.write("[%s] %s\n" % (dt.datetime.now().strftime("%Y-%m-%d %H:%M"), msg))


def notify(msg):
    subprocess.run(["osascript", "-e", 'display notification "%s" with title "Learning vault" sound name "Glass"'
                    % msg.replace('"', "'").replace("\\", "")])


def run_claude(prompt):
    r = subprocess.run(
        [CLAUDE, "-p", prompt, "--permission-mode", "acceptEdits", "--allowedTools", *TOOLS.split()],
        cwd=str(VAULT), capture_output=True, text=True, timeout=1800,
    )
    log("claude exit=%d\n%s\n%s" % (r.returncode, r.stdout[-3000:], r.stderr[-2000:]))
    return r.returncode == 0, r.stdout.strip()


def new_text(old, new):
    """Lines inserted or changed in `new` relative to `old` (deletions ignored)."""
    a, b = old.splitlines(), new.splitlines()
    chunks = []
    for tag, _, _, j1, j2 in difflib.SequenceMatcher(None, a, b, autojunk=False).get_opcodes():
        if tag in ("insert", "replace"):
            chunk = "\n".join(b[j1:j2]).strip()
            if chunk:
                chunks.append(chunk)
    return chunks


PROCESS_PROMPT = """You are running unattended in the background (no human is watching; never ask questions).

Below is NEW text Pranay just added to his running learning log (an Apple Note, sometimes typed on
his phone, so expect typos and fragments). Process it into the vault:
follow CLAUDE.md and the steps in .claude/skills/learn/SKILL.md for every idea in it, with these
changes for unattended mode:
- Never ask a clarifying question. If something is too cryptic to interpret, don't guess —
  list it under "Couldn't interpret" in the report.
- If text is clearly not something learned (a to-do, a stray character), skip it silently.
- Don't edit "Learning Log.md" or the Apple Note.
- Don't edit domain maps (e.g. maps/Ecology.md) or maps/Home.md: a script rebuilds them from
  note tags after you finish. DO add notes to fitting theme maps, and create a theme map
  (frontmatter `tags: [map, theme]`) when CLAUDE.md's rule for one is met.

Finally, update "What's new.md" in the vault root: insert a new section at the TOP (below the
file's title line), newest first, formatted as:

## <YYYY-MM-DD HH:MM>
- **New:** [[Note]] — one-line gist   (one bullet per note created)
- **Updated:** [[Note]] — what was added
- **Connected:** [[A]] ↔ [[B]] — the reason, briefly
- **Worth a look:** factual concerns about what he wrote, possible connections you weren't sure enough to write, or open questions
- **Couldn't interpret:** "<quoted text>" — what you need to know

Omit empty bullet types. Keep it short and scannable. Then reply with one plain sentence
summarizing (e.g. "2 new notes, 3 connections") — this becomes a desktop notification.

NEW TEXT:
<<<
%s
>>>
"""

AUTO_MARK = "_Auto-generated from note tags after each run. Don't edit by hand._"


def note_info(path):
    text = path.read_text(encoding="utf-8")
    tags = []
    m = re.search(r"^tags:\s*\[(.*?)\]", text, re.M)
    if m:
        tags = [t.strip().strip("\"'") for t in m.group(1).split(",") if t.strip()]
    m = re.search(r"\*\*In one line:\*\*\s*(.+)", text)
    gist = m.group(1).strip() if m else ""
    if len(gist) > 160:
        gist = gist[:157].rsplit(" ", 1)[0] + "…"
    return tags, gist


def build_maps():
    """Rebuild one map per domain tag, plus maps/Home.md. Theme maps are left alone."""
    maps = VAULT / "maps"
    maps.mkdir(exist_ok=True)
    by_tag = {}
    for p in sorted((VAULT / "notes").glob("*.md"), key=lambda p: p.stem.lower()):
        tags, gist = note_info(p)
        for t in tags:
            by_tag.setdefault(t, []).append((p.stem, gist))

    def title(tag):
        return tag.replace("-", " ").title().replace(" ", "-") if "-" in tag else tag.title()

    domain_names = set()
    for tag, items in by_tag.items():
        name = title(tag)
        domain_names.add(name)
        lines = ["---", "tags: [map, domain]", "---", "", "# " + name, "", AUTO_MARK, ""]
        lines += ["- [[%s]]%s" % (n, " — " + g if g else "") for n, g in items]
        (maps / (name + ".md")).write_text("\n".join(lines) + "\n", encoding="utf-8")

    themes = []
    for p in sorted(maps.glob("*.md")):
        if p.stem == "Home" or p.stem in domain_names:
            continue
        if AUTO_MARK in p.read_text(encoding="utf-8"):
            p.unlink()  # domain map whose tag no longer exists
        else:
            themes.append(p.stem)

    home = ["---", "tags: [map]", "---", "", "# Home", "", AUTO_MARK, "",
            "Latest activity: [[What's new]]", "", "## Themes"]
    home += ["- [[%s]]" % t for t in themes] or ["- (none yet)"]
    home += ["", "## Fields"]
    home += ["- [[%s]] (%d)" % (title(t), len(by_tag[t])) for t in sorted(by_tag, key=lambda t: -len(by_tag[t]))]
    (maps / "Home.md").write_text("\n".join(home) + "\n", encoding="utf-8")


def read_apple_note():
    script = ('tell application "Notes" to if exists note "%s" then return plaintext of note "%s"'
              % (NOTE_NAME, NOTE_NAME))
    r = subprocess.run(["osascript", "-e", script], capture_output=True, text=True, timeout=60)
    if r.returncode != 0:
        log("couldn't read Apple Note: " + r.stderr.strip())
        return None
    return r.stdout.rstrip("\n") or None


def pending_chunks():
    """New text from each source. Returns ([(snapshot_path, current_text), ...], chunks)."""
    sources = [(NOTE_SNAPSHOT, read_apple_note()),
               (SNAPSHOT, LOG.read_text(encoding="utf-8") if LOG.exists() else None)]
    updates, chunks = [], []
    for snap, current in sources:
        if current is None:
            continue
        old = snap.read_text(encoding="utf-8") if snap.exists() else ""
        new = new_text(old, current)
        if new:
            updates.append((snap, current))
            chunks += new
    return updates, chunks


def worker():
    lock = open(LOCK, "w")
    try:
        fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
    except BlockingIOError:
        return
    updates, chunks = pending_chunks()
    if not chunks:
        return
    log("processing %d new chunk(s)" % len(chunks))
    ok, summary = run_claude(PROCESS_PROMPT % "\n\n---\n\n".join(chunks))
    if ok:
        for snap, current in updates:
            snap.write_text(current, encoding="utf-8")
        build_maps()
        notify(summary.splitlines()[-1][:200] if summary else "Log processed")
    else:
        notify("Processing failed. Nothing was lost; run learn again.")


def main():
    os.environ["PATH"] = str(pathlib.Path.home() / ".local" / "bin") + ":/opt/homebrew/bin:/usr/bin:/bin:" + os.environ.get("PATH", "")
    (VAULT / "meta").mkdir(exist_ok=True)
    if "--worker" in sys.argv:
        return worker()
    if "--maps" in sys.argv:
        build_maps()
        return print("Maps rebuilt.")

    with open(LOCK, "w") as lock:
        try:
            fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
            fcntl.flock(lock, fcntl.LOCK_UN)
        except BlockingIOError:
            return print("Still processing your last batch. Run learn again once you get the notification.")
    _, chunks = pending_chunks()
    if not chunks:
        return print("Nothing new in the log.")
    subprocess.Popen([sys.executable, str(pathlib.Path(__file__).resolve()), "--worker"],
                     stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
                     start_new_session=True)
    n = len(chunks)
    print("Got %d new entr%s. Processing in the background; you'll get a notification when it's done."
          % (n, "y" if n == 1 else "ies"))


if __name__ == "__main__":
    main()
