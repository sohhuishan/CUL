#!/usr/bin/env python3
"""Stop hook: auto-commit/push findings; block once if a substantial session logged none."""
import json, os, subprocess, sys, time

try:
    data = json.load(sys.stdin)
except Exception:
    data = {}
root = data.get("cwd") or os.getcwd()
sid = data.get("session_id", "nosession")
active = data.get("stop_hook_active", False)

def git(*a, check=False):
    return subprocess.run(["git", "-C", root, *a], capture_output=True, text=True)

if git("rev-parse", "--git-dir").returncode != 0:
    sys.exit(0)
marker = os.path.join(root, ".git", f"findings_logged_{sid}")

# 1. Commit + push any pending findings.
pending = git("status", "--porcelain", "--", "docs/findings", "docs/FINDINGS.md").stdout.strip()
if pending:
    git("add", "docs/findings", "docs/FINDINGS.md")
    msg = "Log findings\n\nCo-Authored-By: Claude <noreply@anthropic.com>"
    git("commit", "-m", msg, "--", "docs/findings", "docs/FINDINGS.md")
    branch = git("rev-parse", "--abbrev-ref", "HEAD").stdout.strip()
    target = "findings" if branch in ("main", "master", "HEAD") else branch
    for delay in (0, 2, 4, 8, 16):
        time.sleep(delay)
        if git("push", "-u", "origin", f"HEAD:refs/heads/{target}").returncode == 0:
            break
    open(marker, "w").write("1")
    sys.exit(0)

# 2a. A findings file dated today already exists (e.g. committed by hand): treat as logged.
import glob, datetime
if glob.glob(os.path.join(root, "docs", "findings", datetime.date.today().isoformat() + "-*.md")):
    open(marker, "w").write("1")
    sys.exit(0)

# 2. Already logged this session, or this is the re-stop after we asked: allow.
if os.path.exists(marker) or active:
    sys.exit(0)

# 3. Substantial session? (>=6 tool calls in transcript)
tp = data.get("transcript_path")
n = 0
if tp and os.path.exists(tp):
    with open(tp, errors="ignore") as f:
        n = sum(line.count('"type":"tool_use"') for line in f)
if n < 6:
    sys.exit(0)

print(json.dumps({
    "decision": "block",
    "reason": ("Before finishing: record this session's findings. Copy docs/findings/_TEMPLATE.md to "
               "docs/findings/<today>-<topic>.md, fill it (Status honest: Confirmed/Hypothesis), and add a "
               "line to docs/FINDINGS.md. If there were genuinely no findings, write a one-line "
               "'no new findings' entry instead. The hook will commit and push it."),
}))
