---
name: release
description: Update or create a CHANGELOG.md from the commits since the last release (git tag based), commit it using the commit skill and create a new release tag. Use when (1) user wants to release a new version, (2) user invokes /release command, (3) user asks to create a new release. Triggers on "release".
allowed-tools: Bash, Read, Write, Edit, Glob, Grep, AskUserQuestion, Skill
---

# Release Skill

Goal: Analyze git commits since the last release to create or update a CHANGELOG.md in [Keep a Changelog](https://keepachangelog.com/) format, commit it using the `/commit` skill, and create a new git tag.

The user input to you can be provided directly by the agent or as a command argument - you **MUST** consider it before proceeding with the prompt (if not empty).

User input:

$ARGUMENTS

## Argument Parsing

Parse the following optional argument from `$ARGUMENTS`:

- A version number (e.g., `1.2.0`, `2025.06.15`) - If provided, use this as the release version directly

Examples:
- `/release` - Determine version interactively
- `/release 1.2.0` - Release as version 1.2.0
- `/release 2025.06.15` - Release as version 2025.06.15

Any text that matches a version-like pattern (`X.Y.Z` for semver, or `YYYY.MM.DD` / `YYYY.M.D` for CalVer) is treated as the version number.

# Execution Steps

## Step 1: Determine the Last Release and Versioning Scheme

1. Run `git tag --sort=-v:refname` to list all tags sorted by version (descending)
2. Identify the latest tag that looks like a version (e.g., `1.0.0`, `2025.06.15`)
3. If no tags exist, this is the **first release** - all commits will be included
4. **Detect the versioning scheme** from existing tags:
   - **CalVer** (date-based): The tag matches the pattern `YYYY.MM.DD` or `YYYY.M.D` where `YYYY` is a plausible year (>= 2000), `MM`/`M` is 1-12, and `DD`/`D` is 1-31. Examples: `2025.6.15`, `2025.01.03`
   - **SemVer**: Any other `X.Y.Z` pattern where the numbers don't resemble a date
   - If no tags exist, default to **SemVer** (CalVer can still be used if the user provides a date-like version in `$ARGUMENTS`)
5. Display the last release tag (or "No previous release found") and the detected versioning scheme to the user

## Step 2: Collect Commits Since Last Release

1. If a previous tag exists, run `git log <last-tag>..HEAD --pretty=format:"%H %s"` to get all commits since that tag
2. If no previous tag exists, run `git log --pretty=format:"%H %s"` to get all commits
3. If there are **no commits** since the last release, inform the user and stop
4. Display a summary: "Found N commits since last release (TAG)"
5. **Determine the GitHub repository URL** for commit links:
   - Run `git remote get-url origin` to get the remote URL
   - Convert SSH URLs (e.g., `git@github.com:owner/repo.git`) to HTTPS form: `https://github.com/owner/repo`
   - Strip any trailing `.git` suffix from HTTPS URLs
   - Store this as the base URL for constructing commit links in the changelog (e.g., `<base-url>/commit/<full-hash>`)

## Step 3: Determine the Release Version

**If a version was provided in `$ARGUMENTS`:**
- Validate it looks like a valid version (semver `X.Y.Z` or calver `YYYY.MM.DD`)
- Use it directly and skip to Step 4

**If no version was provided, the behavior depends on the detected versioning scheme:**

### CalVer (date-based versioning)

1. Determine today's date as the version: `YYYY.MM.DD` (no zero-padding for month/day to match common CalVer conventions, but match the zero-padding style of existing tags if any exist)
2. Check if a tag for today's date already exists
   - If it does **not** exist: suggest today's date as the version
   - If it **does** exist: append an incrementing suffix (e.g., `2025.6.15.1`, `2025.6.15.2`) to distinguish multiple releases on the same day
3. Use `AskUserQuestion` to confirm:
   - "Use YYYY.MM.DD" - with the calculated version shown
   - "Use YYYY.MM.DD.N" - only shown if today's date tag already exists, with the incremented suffix

### SemVer (semantic versioning)

1. Determine the current version from the last tag (or `0.0.0` if no tags exist)
2. Calculate the three possible next versions:
   - **Major**: Increment major, reset minor and patch (e.g., `1.2.3` -> `2.0.0`)
   - **Minor**: Increment minor, reset patch (e.g., `1.2.3` -> `1.3.0`)
   - **Patch**: Increment patch (e.g., `1.2.3` -> `1.2.4`)
3. Use `AskUserQuestion` to let the user choose:
   - "Major (X.0.0)" - with the calculated version shown
   - "Minor (X.Y.0)" - with the calculated version shown
   - "Patch (X.Y.Z)" - with the calculated version shown

## Step 4: Categorize Commits

Categorize each commit based on its gitmoji or conventional commit prefix into [Keep a Changelog](https://keepachangelog.com/) sections:

| Category | Gitmoji matches | Conventional commit matches |
|---|---|---|
| **Added** | `:sparkles:`, `:tada:`, `:heavy_plus_sign:`, `:construction_worker:` | `feat` |
| **Changed** | `:recycle:`, `:art:`, `:zap:`, `:lipstick:`, `:building_construction:` | `refactor`, `perf`, `style` |
| **Deprecated** | `:wastebasket:` | `deprecate` |
| **Removed** | `:fire:`, `:heavy_minus_sign:` | `remove` |
| **Fixed** | `:bug:`, `:ambulance:`, `:pencil2:`, `:adhesive_bandage:` | `fix` |
| **Security** | `:lock:`, `:rotating_light:` | `security` |

Commits that don't match any category go into **Changed** as a fallback.

When categorizing:
- Strip the gitmoji prefix (both Unicode emoji and `:code:` form) from the commit message for the changelog entry
- Strip conventional commit prefixes (e.g., `fix:`, `feat(scope):`) from the message
- Clean up the message to read naturally as a changelog bullet point
- **Keep the full commit hash** associated with each entry for generating commit links
- Derive a **short hash** (first 7 characters) from the full hash for display in the changelog

## Step 5: Generate CHANGELOG Content

Generate a changelog entry following the [Keep a Changelog](https://keepachangelog.com/) format.

**If a CHANGELOG.md already exists:**
1. Read the existing file
2. Insert the new release section **after** the `## [Unreleased]` section (or after the header if no Unreleased section exists)
3. If there is an `## [Unreleased]` section with content, move its content into the new release section and leave `## [Unreleased]` empty
4. Preserve all existing content below

**If no CHANGELOG.md exists:**
1. Create a new file with the full Keep a Changelog structure

**Format for the new release section:**
```markdown
## [X.Y.Z] - YYYY-MM-DD

### Added
- Description of added feature ([abc1234])
- Another added feature ([def5678])

### Changed
- Description of change ([ghi9012])

### Fixed
- Description of fix ([jkl3456])

[abc1234]: https://github.com/owner/repo/commit/abc1234abc1234abc1234abc1234abc1234abc1234
[def5678]: https://github.com/owner/repo/commit/def5678def5678def5678def5678def5678def5678
[ghi9012]: https://github.com/owner/repo/commit/ghi9012ghi9012ghi9012ghi9012ghi9012ghi9012
[jkl3456]: https://github.com/owner/repo/commit/jkl3456jkl3456jkl3456jkl3456jkl3456jkl3456
```

**Rules:**
- Only include sections that have entries (don't add empty sections)
- Use today's date in `YYYY-MM-DD` format
- Each entry should be a concise, human-readable description
- Start each entry with an uppercase letter
- Don't end entries with a period
- Append the short commit hash as a Markdown reference-style link suffix to each entry: `([short-hash])`
- Collect all reference link definitions at the **bottom of the release section** (after all category subsections), one per line: `[short-hash]: <base-url>/commit/<full-hash>`
- Use the GitHub repository URL determined in Step 2 as the base URL

**Full file structure (for new files):**

If using SemVer:
```markdown
# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/),
and this project adheres to [Semantic Versioning](https://semver.org/).

## [Unreleased]

## [X.Y.Z] - YYYY-MM-DD

### Added
- Description of feature ([abc1234])

[abc1234]: https://github.com/owner/repo/commit/abc1234...
```

If using CalVer:
```markdown
# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/),
and this project adheres to [Calendar Versioning](https://calver.org/).

## [Unreleased]

## [YYYY.MM.DD] - YYYY-MM-DD

### Added
- Description of feature ([abc1234])

[abc1234]: https://github.com/owner/repo/commit/abc1234...
```

## Step 6: Update Project Version in Manifest Files

After generating the changelog, update the version field in any detected project manifest files. Check for the following files **in the repository root**:

| Ecosystem | File | Field to update | How to update |
|---|---|---|---|
| **Rust** | `Cargo.toml` | `version = "X.Y.Z"` under `[package]` | Edit the `version` value in the `[package]` section. Do **not** touch `version` fields in `[dependencies]` or other sections |
| **npm** | `package.json` | `"version": "X.Y.Z"` | Edit the top-level `"version"` field |
| **Yarn/npm** | `package-lock.json` | `"version": "X.Y.Z"` | Edit the top-level `"version"` field (the root package entry). If it exists, it must stay in sync with `package.json` |
| **Yarn** | `yarn.lock` | No version field | Do **not** edit - Yarn lock files don't contain a project version |

**Detection rules:**
1. Use Glob to check which of these files exist in the repository root
2. Only update files that are found - skip silently if a manifest doesn't exist
3. If **multiple** manifests exist (e.g., a Rust project with a `package.json` for tooling), update **all** of them
4. If **no** manifest files are found, skip this step silently

**Update rules:**
- Read the file first, then use Edit to change only the version field
- For `Cargo.toml`: only update the `version` under `[package]`, not workspace or dependency versions
- For `package.json` / `package-lock.json`: only update the top-level `"version"` key, not nested dependency versions
- Preserve all other content and formatting exactly as-is
- If a `Cargo.lock` exists and `Cargo.toml` was updated, run `cargo update --workspace` to regenerate it (so the lock file stays in sync)

**Display:** List which manifest files were updated (or note that none were found) so the user can see this in the Step 7 preview.

## Step 7: Preview and Confirm

1. Show the user the generated changelog section (the new release block only, not the entire file)
2. Show the version number and tag that will be created
3. List which manifest files were updated with the new version (or note "No manifest files found" if none)
4. Use `AskUserQuestion` for confirmation:
   - "Yes, create release" - Proceed with writing, committing, and tagging
   - "Edit changelog" - Let the user request changes to the changelog entries
   - "Cancel" - Abort the release

**Option handling:**
- **"Yes, create release"**: Proceed to Step 8
- **"Edit changelog"**: Ask what to change, apply changes, then ask for confirmation again
- **"Cancel"**: Inform the user the release was cancelled and stop

## Step 8: Write CHANGELOG and Commit

1. Write the updated CHANGELOG.md to disk (using Write or Edit tool)
2. Stage **all** release-related files:
   - `git add CHANGELOG.md`
   - Stage any manifest files that were updated in Step 6 (e.g., `git add Cargo.toml`, `git add package.json package-lock.json`)
   - If `Cargo.lock` was regenerated, stage it too: `git add Cargo.lock`
3. Use the `/commit` skill to commit the staged changes by invoking the Skill tool with `skill: "commit"` and passing the following as args: `--emoji :bookmark: Release X.Y.Z`
   - The `:bookmark:` emoji is the standard gitmoji for release/version tags
   - Let the commit skill handle the commit creation with its own workflow

## Step 9: Create Git Tag

1. After the commit is created successfully, create an **annotated** tag:
   ```bash
   git tag -a "X.Y.Z" -m "Release X.Y.Z"
   ```
   - Use **plain** format (no `v` prefix): `1.0.0`, not `v1.0.0`
   - Use the user's GPG key for signing the tag. If this fails, ask the user to provide the GPG key and unlock it so that the tag can be signed
   - You **MUST** never use `--no-sign` without user confirmation
2. Verify the tag was created: `git tag -l "X.Y.Z"`
3. Display a success summary:
   ```
   Release X.Y.Z created successfully!
   - CHANGELOG.md updated
   - Version updated in: <list of manifest files, or "no manifest files">
   - Commit created
   - Tag X.Y.Z created
   ```

## Error Handling

- If `git tag` fails, inform the user and suggest checking if the tag already exists
- If the commit skill fails, do not create the tag - inform the user and stop
- If CHANGELOG.md writing fails, do not commit or tag - inform the user and stop
- At any point, if the user cancels, cleanly stop without leaving partial state
