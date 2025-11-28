---
allowed-tools: Bash(tree:*), Bash(mkdir:*), Bash(for:*), Bash(head:*), Bash(cat:*), Bash(done), Bash(find:*), Bash(sqlx migrate:*), Bash(cargo check:*), Bash(SQLX_OFFLINE=true cargo check:*), Bash(npm run:*), Bash(npm install) Bash(git add:*), Bash(git status:*), Bash(git commit:*), Bash(npx tsc:*), Bash(npx eslint:*), Bash(docker-compose:*), Bash(cargo build:*), Bash(curl:*), Bash(docker logs:*), Bash(lsof:*), Bash(npm run dev:*), mcp__playwright__browser_navigate, mcp__playwright__browser_click, mcp__playwright__browser_type, mcp__playwright__browser_snapshot, mcp__playwright__browser_console_messages, mcp__playwright__browser_take_screenshot
description: Implement a user story which was already planed
---

## Context

- Current git status: !`git status`
- Current git diff (staged and unstaged changes): !`git diff HEAD`
- Current branch: !`git branch --show-current`
- Recent commits: !`git log --oneline -10`
- If you unsure, rather ask than guess.
- The scope relates to the part of the project where the change was made (e.g. `backend`, `frontend`, etc.).
- Use the detailed instructions in the `CLAUDE.md` file in the root directory of the repository. 

## Your task

Please implement the following user story: $ARGUMENTS