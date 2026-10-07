#!/usr/bin/env python3
"""Print a git tree hash for a worktree without changing it. Python 3.9+, stdlib only.

  python3 snapshot.py [path]   path defaults to the current directory

The tree holds tracked files and untracked files that .gitignore does not
exclude, as they are on disk now. It is built in a temporary index, so the real
index, refs, stash, and worktree are unchanged. Compare two snapshots with
`git diff <before> <after> -- <paths>` and read a file as it was with
`git show <tree>:<path>`. Unreferenced trees are pruned by git gc after its
expiry period, two weeks by default.

Blind spots: a submodule is recorded only as its checked-out commit, changes
to ignored files are invisible, entries marked assume-unchanged or
skip-worktree keep their indexed content, and every non-ignored untracked file
is hashed into the object store, through any clean filters such as LFS.
"""
import os, shutil, subprocess, sys, tempfile


def git(*args, cwd, env=None):
    return subprocess.run(["git", *args], cwd=cwd, env=env, check=True,
                          capture_output=True, text=True).stdout.strip()


def main():
    where = sys.argv[1] if len(sys.argv) > 1 else "."
    if not shutil.which("git"):
        sys.exit("snapshot: git is not installed")
    try:
        top = git("rev-parse", "--show-toplevel", cwd=where)
        index = os.path.join(top, git("rev-parse", "--git-path", "index", cwd=top))
    except (OSError, subprocess.CalledProcessError):
        sys.exit("snapshot: not a git worktree")
    with tempfile.TemporaryDirectory() as tmp:
        temp_index = os.path.join(tmp, "index")
        if os.path.exists(index):
            shutil.copyfile(index, temp_index)
        env = {**os.environ, "GIT_INDEX_FILE": temp_index}
        try:
            git("add", "-A", cwd=top, env=env)
            print(git("write-tree", cwd=top, env=env))
        except subprocess.CalledProcessError as error:
            sys.exit(f"snapshot: {error.stderr.strip() or error}")


if __name__ == "__main__":
    main()
