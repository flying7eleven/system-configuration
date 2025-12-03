---
allowed-tools: Bash(git add:*), Bash(git status:*), Bash(git commit:*)
description: Extract user stories from an EPIC.
argument-hint: [epic] [story_folder]
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

I want to build a product which is described in @specs/product/vision.md for the product vision and @specs/product/glossary.md for the glossary. Please extract user stories from $1 and write them into the `$2` folder. Those stories should be detailed enough to be used for implementation. Try to use vertical slices for the stories. You can use all configured subagents and MCPs (like Playwright). If you have questions ask rather than guess.
