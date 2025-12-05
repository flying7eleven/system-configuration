---
allowed-tools: Read, Write, Edit, Glob, Grep, Task, TodoWrite, AskUserQuestion, EnterPlanMode, mcp__playwright, Bash(git add:*), Bash(git commit:*), Bash(git checkout:*), Bash(git branch:*), Bash(git restore:*), Bash(git status:*), Bash(git log:*), Bash(git diff:*), Bash(git reset:*), Bash(docker exec:*), Bash(docker-compose up:*), Bash(DOCKER_DEFAULT_PLATFORM=linux/amd64 docker-compose up:*), Bash(docker rm:*), Bash(docker-compose down:*), Bash(docker volume ls:*), Bash(lsof:*), Bash(curl:*), Bash(sort:*), Bash(shasum:*), Bash(npx eslint:*), Bash(npm run build:*), Bash(npm run dev:*), Bash(npm run lint:*), Bash(npm test:*), Bash(cargo fmt:*), Bash(cargo clippy:*), Bash(cargo sqlx prepare:*), Bash(cargo check:*), Bash(cargo test:*), Bash(RUST_LOG=info cargo run:*), Bash(RUST_LOG=debug cargo run:*), Bash(cargo clean:*), Bash(sqlx migrate:*), Bash(python3:*), Bash(psql:*)
argument-hint: Story ID (e.g., US-42) or filename (e.g., US-42-user-login.md)
description: Implement a user story which was already planned
---

## Context

### Documentation

**Note:** The paths below assume a standard project structure. Adjust if your project uses different conventions.

- Product vision: @specs/product/vision.md
- Glossary: @specs/product/glossary.md
- Architecture:
    - API: @specs/product/architecture/api.md
    - Components: @specs/product/architecture/components.md
    - Data-flow: @specs/product/architecture/data-flow.md
    - Database: @specs/product/architecture/database.md
    - System overview: @specs/product/architecture/system-overview.md
- Project conventions: @CLAUDE.md
- EPICS are stored in @specs/planning/epics
- Stories are stored in @specs/planning/stories

**Important:** If any of the above files are missing, stop and ask the user to initialize the documentation first.

### Guidelines

- If you are unsure about requirements, ask rather than guess
- Follow conventions in `CLAUDE.md`
- If you gain new knowledge during implementation (e.g., gotchas, undocumented behaviors, useful patterns), persist it to `CLAUDE.md` under an appropriate section

## Your Task

Implement the user story: **$ARGUMENTS**