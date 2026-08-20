"""Git helpers used by RSSPrune."""

import os
import subprocess
from pathlib import Path


class GitError(RuntimeError):
 pass


def run_git(args, cwd=None):
 result = subprocess.run(
 ["git", *args],
 cwd=cwd or str(Path.cwd()),
 capture_output=True,
 text=True,
 )
 if result.returncode != 0:
 raise GitError(result.stderr.strip() or result.stdout.strip())
 return result.stdout.strip()


def is_repo(path=None):
 try:
 run_git(["rev-parse", "--is-inside-work-tree"], cwd=path)
 return True
 except GitError:
 return False


def current_branch(path=None):
 try:
 return run_git(["rev-parse", "--abbrev-ref", "HEAD"], cwd=path)
 except GitError:
 return ""


def recent_commits(limit=20, path=None):
 try:
 output = run_git(["log", f"-{limit}", "--pretty=format:%h|%an|%s"], cwd=path)
 except GitError:
 return []
 commits = []
 for line in output.splitlines():
 parts = line.split("|", 2)
 if len(parts) == 3:
 commits.append({"hash": parts[0], "author": parts[1], "subject": parts[2]})
 return commits


def dirty_files(path=None):
 try:
 output = run_git(["status", "--porcelain"], cwd=path)
 except GitError:
 return []
 return [line[3:] for line in output.splitlines() if line.strip()]


def ensure_repo(path):
 path = Path(path)
 path.mkdir(parents=True, exist_ok=True)
 if not is_repo(path):
 run_git(["init"], cwd=str(path))
 return path