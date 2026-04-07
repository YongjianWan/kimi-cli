---
name: workspace-audit
description: Audit project health, dependencies, and code quality using workspace-bridge-cli. Use when starting work on a codebase, before refactoring, or when investigating technical debt.
---

# Workspace Audit

Analyze project structure, health metrics, and potential issues before making changes.

## When to Use

- **Starting on a new codebase** - Get the lay of the land
- **Before refactoring** - Identify hotspots and risky areas
- **Code review prep** - Understand impact radius of changes
- **Technical debt assessment** - Find dead code, cycles, orphans

## Tools

| Tool | Purpose | Use When |
|------|---------|----------|
| `WorkspaceAuditSummary` | Quick health overview | First contact with codebase |
| `WorkspaceAuditFile` | Single file impact | Modifying a specific file |
| `WorkspaceAuditDiff` | Git change analysis | Reviewing PRs, staged changes |
| `WorkspaceAuditOverview` | Deep project analysis | Architecture review, planning |

## Workflow

### 1. Initial Assessment

```
WorkspaceAuditSummary → understand severity and key metrics
```

Look for:
- Health score (0-5)
- Severity level (high/medium/low)
- Dead exports count
- Circular dependencies
- Missing hygiene (LICENSE, CI, tests)

### 2. Before Modifying a File

```
WorkspaceAuditFile --file <path> → check impact radius
```

Review:
- Direct dependents
- Affected tests
- Import/export relationships

### 3. Review Changes

```
WorkspaceAuditDiff → analyze git changes
```

Check:
- Changed files impact
- Test coverage affected
- Risk assessment

### 4. Deep Dive (Optional)

```
WorkspaceAuditOverview → hotspots, orphans, stability
```

## Interpreting Results

### Severity Levels

| Level | Meaning | Action |
|-------|---------|--------|
| high | Critical issues | Fix before major changes |
| medium | Notable debt | Plan cleanup |
| low | Minor issues | Address when convenient |

### Health Score

| Score | Interpretation |
|-------|----------------|
| 5/5 | Excellent - all hygiene checks pass |
| 4/5 | Good - minor gaps |
| 3/5 | Fair - some important items missing |
| 2/5 | Poor - major gaps (LICENSE, CI, tests) |
| 1/5 | Critical - minimal project structure |
| 0/5 | No recognizable project |

### Dead Exports

Exports not imported elsewhere. **Candidates for removal**, not automatic deletions:
- Check if used dynamically
- Verify not part of public API
- Confirm not used by external consumers

### Circular Dependencies

**Break before broad refactors.** Cycles indicate coupling that can cause:
- Unexpected side effects
- Harder testing
- Initialization order bugs

## Example Session

```
User: I need to refactor the auth module

→ WorkspaceAuditSummary (assess overall health)
→ WorkspaceAuditFile --file src/auth.ts (check impact)
→ (make changes)
→ WorkspaceAuditDiff (verify change scope)
```

## Prerequisites

workspace-bridge-cli must be installed:

```bash
npm install -g workspace-bridge-cli
```
