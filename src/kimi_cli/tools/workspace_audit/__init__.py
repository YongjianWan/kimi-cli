"""Workspace audit tools via workspace-bridge-cli."""

from __future__ import annotations

import json
import platform
import shutil
import subprocess
from typing import Any, override

from kosong.tooling import CallableTool2, ToolReturnValue
from pydantic import BaseModel, Field

from kimi_cli.tools.utils import ToolResultBuilder


def _find_workspace_bridge() -> str | None:
    """Find workspace-bridge executable."""
    system = platform.system()
    if system == "Windows":
        for ext in [".cmd", ".ps1", ".exe", ""]:
            cmd = f"workspace-bridge{ext}"
            if shutil.which(cmd):
                return cmd
    return shutil.which("workspace-bridge")


def _run_bridge(command: str, cwd: str | None = None) -> dict[str, Any]:
    """Run workspace-bridge CLI command."""
    wb_cmd = _find_workspace_bridge()
    if not wb_cmd:
        err = "workspace-bridge not found. Run: npm install -g workspace-bridge-cli"
        return {"ok": False, "error": err}
    
    cmd = [wb_cmd, command, "--json"]
    if cwd:
        cmd.extend(["--cwd", cwd])
    
    system = platform.system()
    try:
        if system == "Windows":
            cmd_str = subprocess.list2cmdline(cmd)
            result = subprocess.run(
                cmd_str,
                capture_output=True,
                text=True,
                timeout=60,
                shell=True,
                encoding='utf-8',
                errors='replace'
            )
        else:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=60,
                encoding='utf-8',
                errors='replace'
            )
        
        if result.returncode != 0:
            return {"ok": False, "error": result.stderr.strip() or "Command failed"}
        
        return json.loads(result.stdout)
    except subprocess.TimeoutExpired:
        return {"ok": False, "error": "Command timed out after 60 seconds"}
    except json.JSONDecodeError:
        return {"ok": False, "error": "Failed to parse JSON output"}
    except Exception as e:
        return {"ok": False, "error": str(e)}


class AuditSummaryParams(BaseModel):
    cwd: str | None = Field(
        default=None,
        description="Target workspace directory (default: current directory)"
    )


class AuditSummary(CallableTool2[AuditSummaryParams]):
    """Get project health summary including health score, dependency status, and critical issues."""
    
    name: str = "WorkspaceAuditSummary"
    description: str = """Get project health summary via workspace-bridge-cli.
    
Returns:
- Health score (0-5)
- Dead export candidates
- Unresolved imports
- Circular dependencies
- Missing hygiene checks (LICENSE, CI, tests, etc.)
"""
    params: type[AuditSummaryParams] = AuditSummaryParams
    
    @override
    async def __call__(self, params: AuditSummaryParams) -> ToolReturnValue:
        builder = ToolResultBuilder()
        result = _run_bridge("audit-summary", params.cwd)
        
        if not result.get("ok"):
            return builder.error(result.get("error", "Unknown error"), brief="Audit failed")
        
        # Format output
        summary = result.get("summary", {})
        health = result.get("health", {})
        
        builder.write(f"Workspace: {result.get('workspaceRoot', 'unknown')}\n\n")
        
        # Health score
        if health:
            builder.write(f"Health Score: {health.get('healthScore', 'N/A')}/5\n")
            builder.write(f"Package Manager: {health.get('packageManager', 'unknown')}\n\n")
        
        # Summary counts
        if summary:
            severity = summary.get('severity', 'unknown')
            counts = summary.get('counts', {})
            builder.write(f"Severity: {severity}\n")
            builder.write(f"Dead Exports: {counts.get('deadExports', 0)}\n")
            builder.write(f"Unresolved Imports: {counts.get('unresolved', 0)}\n")
            builder.write(f"Circular Dependencies: {counts.get('cycles', 0)}\n")
            builder.write(f"Missing Hygiene: {counts.get('missingHygieneChecks', 0)}\n\n")
            
            next_steps = summary.get('nextSteps', [])
            if next_steps:
                builder.write("Recommendations:\n")
                for step in next_steps:
                    builder.write(f"- {step}\n")
        
        return builder.ok()


class AuditFileParams(BaseModel):
    file: str = Field(description="Path to the file to analyze")
    cwd: str | None = Field(default=None, description="Target workspace directory")


class AuditFile(CallableTool2[AuditFileParams]):
    """Analyze impact radius and affected tests for a specific file."""
    
    name: str = "WorkspaceAuditFile"
    description: str = "Analyze file impact radius and affected tests via workspace-bridge-cli."
    params: type[AuditFileParams] = AuditFileParams
    
    @override
    async def __call__(self, params: AuditFileParams) -> ToolReturnValue:
        builder = ToolResultBuilder()
        
        cmd = f"audit-file --file {params.file}"
        result = _run_bridge(cmd, params.cwd)
        
        if not result.get("ok"):
            return builder.error(result.get("error", "Unknown error"), brief="Audit failed")
        
        builder.write(json.dumps(result, indent=2, ensure_ascii=False))
        return builder.ok()


class AuditDiffParams(BaseModel):
    cwd: str | None = Field(default=None, description="Target workspace directory")


class AuditDiff(CallableTool2[AuditDiffParams]):
    """Analyze Git changes and their impact on the codebase."""
    
    name: str = "WorkspaceAuditDiff"
    description: str = "Analyze Git changes and impact via workspace-bridge-cli."
    params: type[AuditDiffParams] = AuditDiffParams
    
    @override
    async def __call__(self, params: AuditDiffParams) -> ToolReturnValue:
        builder = ToolResultBuilder()
        result = _run_bridge("audit-diff", params.cwd)
        
        if not result.get("ok"):
            return builder.error(result.get("error", "Unknown error"), brief="Audit failed")
        
        builder.write(json.dumps(result, indent=2, ensure_ascii=False))
        return builder.ok()


class AuditOverviewParams(BaseModel):
    cwd: str | None = Field(default=None, description="Target workspace directory")


class AuditOverview(CallableTool2[AuditOverviewParams]):
    """Get project panoramic view including hotspots, stability trends, and orphan files."""
    
    name: str = "WorkspaceAuditOverview"
    description: str = "Get project panoramic view via workspace-bridge-cli."
    params: type[AuditOverviewParams] = AuditOverviewParams
    
    @override
    async def __call__(self, params: AuditOverviewParams) -> ToolReturnValue:
        builder = ToolResultBuilder()
        result = _run_bridge("audit-overview", params.cwd)
        
        if not result.get("ok"):
            return builder.error(result.get("error", "Unknown error"), brief="Audit failed")
        
        builder.write(json.dumps(result, indent=2, ensure_ascii=False))
        return builder.ok()
