---
allowed-tools: Read, Write, Edit, Glob, Grep, Task, TodoWrite, AskUserQuestion
description: Extract user stories from an EPIC.
argument-hint: <epic>
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
- Existing EPICs: @specs/planning/epics/

**Important:** If product vision or glossary files are missing, stop and ask the user to initialize the documentation first.

### Guidelines

- If you are unsure about requirements, ask rather than guess
- Follow conventions in @CLAUDE.md
- Review existing EPICs and stories for style consistency before writing
- Use the TodoWrite tool to track your progress

## Arguments

- `<epic>` (required): Path to the EPIC file to extract stories from
  If no EPIC path is provided, list available EPICs from `specs/planning/epics/` and ask the user to select one.
- Stories should be stored in @specs/planning/stories/

## Story Format

Each user story should follow this structure:

### Filename Convention

`US-{number}-{short-kebab-title}.md` (e.g., `US-001-user-login.md`)

### Story Numbering

- Check existing stories in `specs/planning/stories/` to determine the next number
- Numbers are global across all EPICs (not per-EPIC)
- Use zero-padded 3-digit format (001, 002, ..., 056, etc.)

### Required Sections

```markdown
# US-{number}: {Title}

**Epic:** [{Epic Title}](../epics/{epic-filename}.md)

**Status:** Not Started
**Priority:** {P0 (Critical) | P1 (High) | P2 (Medium) | P3 (Low)}
**Story Points:** {1-8, Fibonacci-ish}
**Assignee:** TBD
**Created:** {YYYY-MM-DD}
**Target:** {Phase/Sprint from EPIC roadmap}

---

## User Story

As a **{user role}**
I want **{goal/desire}**
So that **{benefit/value}**

---

## Context

{Background information explaining why this story exists, current state, and how it fits into the larger feature. This helps implementers understand the "why" behind the story.}

---

## Acceptance Criteria

### Functional Requirements

- [ ] {Criterion 1}
- [ ] {Criterion 2}
- [ ] ...

### Non-Functional Requirements

- [ ] {Performance, accessibility, responsiveness requirements}

---

## Technical Implementation

### {Component/Layer Name}

**File:** `{path/to/file.ext}`

{Code snippets, interface definitions, SQL schemas, or implementation guidance as appropriate}

---

## Dependencies

### Blocking

- {Stories or tasks that must be completed first}

### Blocked Stories

This story blocks:

- {Stories that depend on this one}

---

## Files to Create/Modify

| File | Action | Description |
|------|--------|-------------|
| `path/to/file.ext` | Create/Modify | Brief description |

---

## Testing Strategy

### Manual Testing Checklist

- [ ] {Test case 1}
- [ ] {Test case 2}

### Automated Testing

{Unit tests, integration tests, E2E tests to write}

---

## Definition of Done

- [ ] All acceptance criteria met
- [ ] Tests written and passing
- [ ] Code reviewed and approved
- [ ] Documentation updated (if applicable)
- [ ] Git commit with gitmoji: `:{emoji}: ({scope}): {message}`

---

## Related Documentation

- [{Link to EPIC}](../epics/{epic-file}.md)
- {Other relevant docs}

---

## Notes

{Implementation notes, edge cases, future enhancements, design decisions}

---

## Changelog

| Date | Version | Changes |
|------|---------|---------|
| {YYYY-MM-DD} | 1.0 | Initial user story created |
```

### Section Guidelines

- **Context**: Always include - explains the "why" and current state
- **Technical Implementation**: Include code snippets for complex stories; can be brief for simple UI changes
- **Testing Strategy**: Always include manual checklist; add automated tests for backend/complex logic
- **Notes**: Use for edge cases, implementation order, design rationale

## Sizing Guidelines

- Each story should be implementable in **1-3 days** of work
- If a story feels larger, break it into smaller vertical slices
- A vertical slice delivers end-to-end value (UI to database) rather than horizontal layers

## Your Task

1. Read and understand the EPIC at **$ARGUMENTS**
2. Identify distinct user stories using vertical slices
3. For each story:
    - Write a complete story file following the format above
    - Ensure acceptance criteria are specific and testable
    - Note dependencies between stories
4. Create a `_index.md` in the story folder listing all stories with a brief summary and suggested implementation order
5. Present a summary of extracted stories to the user for review

If anything in the EPIC is ambiguous, ask for clarification before creating stories.
