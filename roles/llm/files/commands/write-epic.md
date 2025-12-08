---
allowed-tools: Read, Write, Edit, Glob, Grep, Task, TodoWrite, AskUserQuestion
argument-hint: <epic description>
description: Write a detailed EPIC for a new feature.
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
- User stories: @specs/planning/stories/{epic-name}

**Important:** If product vision or glossary files are missing, stop and ask the user to initialize the documentation first.

### Guidelines

- If you are unsure about requirements, ask rather than guess
- Follow conventions in @CLAUDE.md
- Review existing EPICs for style consistency before writing
- Use the TodoWrite tool to track your progress

## Your Task

Write a detailed EPIC based on: **$ARGUMENTS**

### Process

1. **Understand the request** - Read the product vision and glossary to understand context
2. **Clarify requirements** - Use AskUserQuestion for any ambiguities
3. **Research** - Check existing EPICs and architecture docs for patterns and constraints
4. **Draft the EPIC** - Follow the template below
5. **Save the file** - Use naming convention `EPIC-NNN-short-description.md` in `specs/planning/epics/`

### EPIC Template

```md
# EPIC: [Title]

## Overview

Brief description of the feature/initiative (2-3 sentences).

## Problem Statement

- What problem does this solve?
- Who is affected?
- What is the current state vs desired state?

## Goals

- [ ] Goal 1
- [ ] Goal 2
- [ ] Goal 3

## Non-Goals (Out of Scope)

- What this EPIC explicitly does NOT cover

## User Personas

Which users/roles are affected by this feature?

## Proposed Solution

High-level description of the approach. Include:

- Key components involved
- Integration points
- Technical considerations

## Acceptance Criteria

- [ ] Criterion 1
- [ ] Criterion 2
- [ ] Criterion 3

## Dependencies

- External systems, APIs, or services
- Other EPICs or features that must be completed first
- Required infrastructure or tooling

## Risks & Mitigations

| Risk | Impact | Likelihood | Mitigation |
|------|--------|------------|------------|
| Risk 1 | High/Medium/Low | High/Medium/Low | How to address |

## Open Questions

- [ ] Question 1
- [ ] Question 2

## References

- Links to related docs, designs, or discussions
```

### Output

Save the completed EPIC to: `specs/planning/epics/EPIC-NNN-<short-description>.md`

Determine the next EPIC number by checking existing files in the epics folder.

---

## Agent Usage

Use the Task tool with specialized agents to gather insights and validate your EPIC. Select agents based on the feature domain:

### Research & Validation Agents

| Agent                | When to Use                                                                    | Example Prompt                                                                                                          |
|----------------------|--------------------------------------------------------------------------------|-------------------------------------------------------------------------------------------------------------------------|
| `architect-reviewer` | Validate technical approach, assess scalability, review architecture decisions | "Review the proposed solution for [feature]. Assess scalability, identify architectural risks, and suggest patterns."   |
| `api-designer`       | EPICs involving API changes or new endpoints                                   | "Analyze existing API patterns in the codebase. Suggest endpoint design for [feature] following current conventions."   |
| `ui-designer`        | User-facing features requiring UX considerations                               | "Review the user flow for [feature]. Identify UX considerations, accessibility requirements, and interaction patterns." |

### Domain Expert Agents

| Agent                | When to Use                                         | Example Prompt                                                                                                             |
|----------------------|-----------------------------------------------------|----------------------------------------------------------------------------------------------------------------------------|
| `backend-developer`  | Server-side features, data processing, integrations | "Analyze the backend architecture for [area]. Identify integration points and technical constraints for [feature]."        |
| `frontend-developer` | UI components, client-side state, browser concerns  | "Review frontend patterns in the codebase. Identify components affected by [feature] and suggest implementation approach." |
| `sql-pro`            | Database schema changes, data modeling, queries     | "Analyze the current database schema. Suggest data model changes for [feature] and assess migration complexity."           |

### Quality & Compliance Agents

| Agent                  | When to Use                                          | Example Prompt                                                                                                             |
|------------------------|------------------------------------------------------|----------------------------------------------------------------------------------------------------------------------------|
| `qa-expert`            | Define testability requirements, acceptance criteria | "Review [feature] requirements. Suggest testability considerations, edge cases, and quality criteria."                     |
| `accessibility-tester` | Features with accessibility implications             | "Assess accessibility requirements for [feature]. Identify WCAG compliance needs and assistive technology considerations." |

### Usage Example

```
Task(
  subagent_type="architect-reviewer",
  prompt="Review the proposed authentication system redesign. Assess: 1) Scalability for 10x user growth, 2) Security patterns alignment, 3) Migration risks from current system. Provide findings for the EPIC."
)
```

### Tips

- **Parallel research**: Launch multiple agents simultaneously for independent concerns (e.g., `architect-reviewer` + `ui-designer` for full-stack features)
- **Be specific**: Include feature context and what findings should inform in the EPIC
- **Iterate**: Use agent findings to refine the Proposed Solution and Risks sections
