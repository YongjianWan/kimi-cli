# Workspace Audit Tools

Built-in tools for project auditing via workspace-bridge-cli.

## Tools

| Tool | Description |
|------|-------------|
| `WorkspaceAuditSummary` | Project health summary |
| `WorkspaceAuditFile` | Single file impact analysis |
| `WorkspaceAuditDiff` | Git change impact analysis |
| `WorkspaceAuditOverview` | Project panoramic view |

## Prerequisites

Install workspace-bridge-cli:

```bash
npm install -g workspace-bridge-cli
```

## Enable

Add to `agents/default/agent.yaml`:

```yaml
tools:
  - "kimi_cli.tools.workspace_audit:AuditSummary"
  - "kimi_cli.tools.workspace_audit:AuditFile"
  - "kimi_cli.tools.workspace_audit:AuditDiff"
  - "kimi_cli.tools.workspace_audit:AuditOverview"
```
