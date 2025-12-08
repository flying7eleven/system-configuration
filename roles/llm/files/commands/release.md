---
allowed-tools: Read, Write, Edit, Glob, Grep, Task, TodoWrite, AskUserQuestion, Bash(npm i:*), Bash(cargo build:*), Bash(git log:*), Bash(git tag:*), Bash(git describe:*), Bash(git remote:*)
description: Prepare the project for release
---

## Context

### Documentation

**Note:** The paths below assume a standard project structure. Adjust if your project uses different conventions.

- Glossary: @specs/product/glossary.md
- Project conventions: @CLAUDE.md
- Existing EPICs: @specs/planning/epics/
- Current changelog: @CHANGELOG.md

#### Finding the Last Release

To find commits since the last tagged release (tagged with `year.month.day` format):

1. Get the latest tag:
   ```bash
   git tag --sort=-creatordate | head -1
   ```

2. List commits since that tag:
   ```bash
   git log <last-tag>..HEAD --oneline
   ```

3. If no tags exist, this is the first release - include all commits or start fresh.

#### Getting the Repository URL

To generate correct commit links, determine the repository URL:
```bash
git remote get-url origin
```
Transform the URL to the web format (e.g., `https://github.com/<owner>/<repo>/commit/`).

#### Changelog Format

Use the https://keepachangelog.com/en/1.1.0/ format.
Do not commit anything, this will be done by someone else.

Here is an example changelog:

```
# Changelog

All notable changes since the last release are documented here.

## [Unreleased]

Nothing so far

## 2025.8.1

### Added
- **(frontend)** Add a dashboard view for the found locations ([1b6b5b7])
- **(frontend)** Add the `leaflet` dependency for displaying maps ([1a64963])
- **(frontend)** Add `prettier` to the dev dependencies ([240436d])
- **(backend)** Add proper CORS header support ([f2170fb])
- **(backend)** Add an initial route for getting the locations ([8dd5584])

### Changed
- **(backend)** Upgrade the used dependencies ([f5e6441], [152de9e])
- **(frontend)** Re-format the frontend code ([9602ad6])
- **(backend)** Improve the release build size ([2f1bdde])

### Fixed
- **(backend)** Use the correct path for caching the target directory ([c26ba0a])
- **(backend)** Use caching when building the backend ([edb33ed])

### Security
- **(backend)** Require authentication for the `/v1/position` route ([42cc73d])

[2f1bdde]: https://github.com/<owner>/<repo>/commit/2f1bdde
[c26ba0a]: https://github.com/<owner>/<repo>/commit/c26ba0a
[edb33ed]: https://github.com/<owner>/<repo>/commit/edb33ed
[42cc73d]: https://github.com/<owner>/<repo>/commit/42cc73d
```

You can summarize commits which are dealing with the same stuff but reference all relating commits to them.

#### Using Subagents to Analyze Complex Changes

When there are many commits or complex feature work spanning multiple domains, use specialized subagents to help analyze and categorize changes:

**Available subagents for release analysis:**

| Subagent | When to Use |
|----------|-------------|
| `backend-developer` | Many backend commits (API changes, database migrations, server-side logic) |
| `frontend-developer` | Many frontend commits (UI components, styling, client-side features) |
| `architect-reviewer` | Significant architectural changes or cross-cutting concerns |

**How to use subagents:**

1. **Identifying feature clusters:** When you see 10+ commits that seem related (e.g., all touching `/src/api/`), spawn a subagent to analyze them:
   ```
   Task(subagent_type="backend-developer", prompt="Analyze these commits and summarize what feature or fix they implement together: <commit-list>")
   ```

2. **Understanding complex changes:** For commits with unclear messages or large diffs:
   ```
   Task(subagent_type="architect-reviewer", prompt="Review the changes in commits <hashes> and provide a user-friendly summary for the changelog")
   ```

3. **Domain-specific categorization:** When unsure whether changes are frontend/backend/infra:
   ```
   Task(subagent_type="frontend-developer", prompt="Which of these commits affect the user interface? <commit-list>")
   ```

**Best practices:**
- Only use subagents when there are 5+ related commits that need consolidation
- Provide the subagent with commit hashes and file paths for context
- Ask for a concise, user-facing summary suitable for the changelog
- Run subagents in parallel for different domains when possible

#### Updating Version Numbers

Update the version numbers of all components to the current date in the format `year.month.day` (e.g., `2025.12.5`).

**Discovering components to update:**
1. Search for `package.json` files (Node.js/frontend projects)
2. Search for `Cargo.toml` files (Rust projects)
3. Search for `pyproject.toml` or `setup.py` files (Python projects)
4. Check the project's CLAUDE.md or README for project-specific conventions

**After updating versions, update lockfiles:**
- For `package.json`: Run `npm i` to update `package-lock.json`
- For `Cargo.toml`: Run `cargo build` to update `Cargo.lock`
- Only run these commands if the corresponding manifest file exists

#### Error Handling

- **No CHANGELOG.md exists:** Create a new one with the example structure above
- **No tags exist:** Treat this as the first release; include relevant commits or start with an empty changelog
- **No version files found:** Skip the version update step and note this in your response
- **Lockfile update fails:** Report the error but continue with other tasks

## Your Task

Prepare the project for the release.
Therefore, create or update the CHANGELOG.md in the root folder of the repository.
After generating the changelog and updating the version numbers, try to build the docker containers which are mentioned in @.github/workflows/docker-release.yml