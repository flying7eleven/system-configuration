---
allowed-tools: Bash(git add:*), Bash(git status:*), Bash(git commit:*)
description: Write a detailed EPIC for a new feature.
---

## Context

- Current git status: !`git status`
- Current git diff (staged and unstaged changes): !`git diff HEAD`
- Current branch: !`git branch --show-current`
- Recent commits: !`git log --oneline -10`
- If you are unsure, rather ask the user than guess.
- The scope relates to the part of the project where the change was made (e.g. `backend`, `frontend`, etc.).
- Use the detailed instructions in the `CLAUDE.md` file in the root directory of the repository.

## Your task

I want to build a product which is described in @specs/product/vision.md for the product vision and @specs/product/glossary.md for the glossary. $ARGUMENTS Create a detailed EPIC in the `specs/planning/epics/` folder which describes the plan. The EPIC should be detailed enough to extract user stories from to implement. You can use all configured subagents and MCPs (like Playwright). If you have questions ask rather than guess.
