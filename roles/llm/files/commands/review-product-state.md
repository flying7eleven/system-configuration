---
allowed-tools: Read, Write, Edit, Glob, Grep, Task, TodoWrite, AskUserQuestion
description: Validate the current implementation against the documentation.
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

## Your Task

### 1. Read Documentation
Read all referenced documentation to understand:
- Product goals and terminology
- Architectural patterns and constraints
- Project conventions and standards

### 2. Locate User Stories
Find all user story files in `@specs/planning/stories/`. User stories should follow the naming convention `US-{ID}-{short-description}.md` (e.g., `US-42-user-login.md`).

If no stories are found, inform the user and exit.

### 3. Validate Each Story Implementation

For each user story, check:

**Existence Check:**
- Does the code referenced in the story exist?
- Are the mentioned files, functions, or components present in the codebase?

**Acceptance Criteria:**
- Review the acceptance criteria defined in each story
- Verify if each criterion is satisfied in the implementation
- Use Grep/Glob to locate relevant code sections

**Architecture Compliance:**
- Does the implementation follow the patterns described in architecture docs?
- Are naming conventions from @CLAUDE.md followed?
- Does it integrate correctly with the data flow and components?

**Test Coverage:**
- Look for corresponding test files (unit, integration, e2e)
- Check if critical paths from acceptance criteria are tested

### 4. Generate Status Report

Create a report at `@specs/planning/implementation-status-report.md` with:

**Format:**
```markdown
# Implementation Status Report
Generated: {date}

## Summary
- Total Stories: X
- Fully Implemented: Y
- Partially Implemented: Z
- Not Started: W

## Story Status

### ✓ Fully Implemented
Stories with all acceptance criteria met, tests passing, and architecture compliance.

### ⚠ Partially Implemented
Stories with some criteria met but missing tests, incomplete features, or minor issues.

### ✗ Not Started
Stories with no implementation found.

## Detailed Findings

### US-{ID}: {Story Title}
**Status:** [Fully Implemented | Partially Implemented | Not Started]
**Files:** {list of related files}

**Acceptance Criteria Status:**
- [✓] Criterion 1: Implemented in {file:line}
- [⚠] Criterion 2: Partially implemented, missing {details}
- [✗] Criterion 3: Not found

**Issues:**
- {List any architecture violations, missing tests, or gaps}

**Recommendations:**
- {Suggested actions to complete or fix}

---

{Repeat for each story}

## Next Steps
{High-level recommendations for closing gaps}
```

### 5. Present Findings
After writing the report, summarize key findings to the user:
- How many stories are fully implemented vs pending
- Top 3-5 critical gaps or issues
- Recommended priorities for closing gaps

## Validation Criteria

A story is considered:
- **Fully Implemented** if:
  - All acceptance criteria are met
  - Code exists and follows architecture patterns
  - Tests cover critical paths
  - Follows project conventions

- **Partially Implemented** if:
  - Some acceptance criteria are met
  - Core functionality exists but incomplete
  - Missing tests or has known issues

- **Not Started** if:
  - No code found for the story
  - No evidence of implementation in the codebase

## Using Specialized Subagents

For comprehensive validation, leverage specialized subagents using the Task tool:

### When to Use Each Subagent

**architect-reviewer** - Use for architecture compliance validation:
- When checking if implementation follows architectural patterns from `@specs/product/architecture/`
- To validate service boundaries, data flow, and component integration
- For assessing technical decisions against system design principles
- Example: `Task tool with subagent_type='architect-reviewer' to validate that the user authentication implementation follows the architecture patterns defined in @specs/product/architecture/system-overview.md`

**qa-expert** - Use for test coverage and quality validation:
- When evaluating test completeness for acceptance criteria
- To assess test strategy and coverage metrics
- For identifying testing gaps and quality issues
- Example: `Task tool with subagent_type='qa-expert' to analyze test coverage for US-42 user login story and verify all acceptance criteria have corresponding tests`

**debugger** - Use for issue investigation:
- When stories are marked "Partially Implemented" due to bugs or errors
- To diagnose why acceptance criteria are not being met
- For root cause analysis of implementation issues
- Example: `Task tool with subagent_type='debugger' to investigate why the password reset flow in US-45 fails under certain conditions`

**api-documenter** - Use for API-related stories:
- When validating API endpoint implementations
- To check if API documentation matches implementation
- For verifying API contracts and schemas
- Example: `Task tool with subagent_type='api-documenter' to validate that the REST API endpoints in US-38 match the API specification in @specs/product/architecture/api.md`

### Workflow Integration

1. **Initial Review Phase**: Read stories and locate code manually
2. **Deep Validation Phase**: Deploy subagents for specialized analysis:
   - Use **architect-reviewer** for all stories touching architecture
   - Use **qa-expert** for all stories requiring test validation
   - Use **debugger** for stories with known issues
   - Use **api-documenter** for API-related stories

3. **Report Generation Phase**: Incorporate subagent findings into the status report

### Example Subagent Usage

```
For US-42 (User Login):
1. Use architect-reviewer to validate authentication flow follows security architecture
2. Use qa-expert to verify test coverage includes happy path, error cases, and edge cases
3. Use api-documenter to ensure login endpoint documentation is accurate

For US-45 (Password Reset):
1. Use debugger to investigate the reported failure in email delivery
2. Use qa-expert to identify missing test cases that would have caught the issue
3. Use architect-reviewer to verify the async email pattern matches system design
```

**Important**: Each subagent has access to Read, Grep, Glob tools and can explore the codebase independently. Provide them with clear context including:
- Story ID and description
- Relevant acceptance criteria
- Paths to documentation and code
- Specific questions to answer