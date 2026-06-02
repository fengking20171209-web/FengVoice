# Git Recovery Guide

## Problem

On Windows, Git HTTPS operations may fail with:
- git-remote-https.exe crash
- .git/index.lock
- .git/FETCH_HEAD permission errors
- tag lock errors

These are usually stale processes or permission locks left after interrupted operations.

## Safe recovery sequence

### 1. Check running Git processes

Get-Process git -ErrorAction SilentlyContinue

### 2. Check lock files

Get-ChildItem .git\*.lock -Force -ErrorAction SilentlyContinue
Test-Path .git\FETCH_HEAD

### 3. Stop stale Git process only if confirmed stale

Stop-Process -Id <PID> -Force

Do not kill unrelated processes.

### 4. Remove stale lock files only if no Git process is running

Remove-Item .git\index.lock -Force -ErrorAction SilentlyContinue
Remove-Item .git\packed-refs.lock -Force -ErrorAction SilentlyContinue

### 5. Verify

git status --short
git fetch --tags origin
git checkout main
git pull origin main
git tag --list "v0.*"

### 6. Full recovery: create a new .git directory

If permission locks persist even after removing lock files, the .git directory itself may have ACL issues. In that case:

Rename-Item .git .git_old
git init
git remote add origin https://github.com/fengking20171209-web/FengVoice.git
git fetch --tags origin
git branch -m master main
git reset --hard origin/main

This preserves the old .git as .git_old for reference until the new one is confirmed working.

## Do not

- git reset
- git rebase
- git push --force
- delete remote branches
- delete remote tags
- repeatedly retry failed push
