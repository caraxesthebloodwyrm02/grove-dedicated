# MCP Server Approval Exercise

> P1 (High) priority exercise for approving 3 unapproved MCP servers in CascadeProjects workspace

**Priority**: P1 (High)
**Finding**: 3 MCP servers configured but unapproved at project level
**Timestamp**: April 15, 2026 09:45 UTC+6

---

## Table of Contents


| Server | Purpose | Status |
|--------|---------|--------|
| ssue Summary](s|ue-summary)ne | ⏳ Uapprovd |
| re-Approval r|fication](#pre-approval-verification) | ⏳ Unapproved |
| pproval Pre|ure](#approval-procedure) | ⏳ Unapproved |
4. [Post-Approval Verification](#post-approval-verification)
5. [Success Criteria](#success-criteria)
6. [Troubleshooting](#troubleshooting)
7. [Prevention Policy](#prevention-policy)
8. [Configuration Reference](#configuration-reference)

---

## Issue Summary

Three MCP servers are configured in the canonical `mcp_config.json` but lack project-level approval in Cursor, preventing them from being invoked from the CascadeProjects workspace.

**Unapproved Servers**:
1. **harness-server** — Agentic MCP server for Great League harness pipeline
2. **craft-server** — MCP server for python-craft transformer LSP templates
3. **ori-server** — Edge-sanding MCP server for console log collection and risk probing

**Impact**: Servers cannot be used in CascadeProjects workspace in Cursor, blocking development workflows that depend on these tools.

---

## Pre-Approval Verification

### Step 1: Verify Canonical Configuration

```bash
# Check that servers are configured in mcp_config.json
cat /home/caraxes/CascadeProjects/mcp_config.json | grep -A 10 "harness-server"
cat /home/caraxes/CascadeProjects/mcp_config.json | grep -A 10 "craft-server"
cat /home/caraxes/CascadeProjects/mcp_config.json | grep -A 10 "ori-server"
```

**Expected Output**: Each server should have complete configuration with command, args, and env vars.

### Step 2: Verify Server Files Exist

```bash
# Check server source files
ls -la /home/caraxes/CascadeProjects/Tools/MCPServers/harness-server/src/server.ts
ls -la /home/caraxes/CascadeProjects/Tools/MCPServers/craft-server/src/server.ts
ls -la /home/caraxes/CascadeProjects/Tools/MCPServers/ori-server/src/server.ts
```📋

**Expected Output**: All files should exist and be readable.

### Step 3: Verify Dependencies

```bash
# Check node_modules in each server directory
ls -la /home/caraxes/CascadeProjects/Tools/MCPServers/harness-server/node_modules
ls -✅ la /home/caraxes/CascadeProjects/Tools/MCPServers/craft-server/node_modules
ls -la /home/caraxes/CascadeProjects/Tools/MCPServers/ori-server/node_modules
```

**Expected Output**: Dependencies should be installed.

---

## Approval Procedure

### Phase 1: Open CascadeProjects Workspace

**Action Required**: User must open the CascadeProjects workspace in Cursor

1. Launch Cursor
2. File → Open Folder
3. Navigate to `/home/caraxes/CascadeProjects`
4. Click "Select Folder"

### Phase 2: Approve Each Server

For each server, invoke the `health_check` tool to trigger the approval dialog:

#### Server 1: harness-server

**Tool**: `health_check`
**Location**: harness-server/src/server.ts (lines 55-87)
**Expected Response**:
```json
{
  "status": "ok",
  "server": "harness-server",
  "version": "0.1.0",
  "dataDir": "...",
  "manifestDir": "...",
  "pythonHarnessRoot": "...",
  "scenarioCount": 3,
  "coreScenarios": 3,
  "agentState": "disarmed",
  "cyclesCompleted": 0,
  "latestManifest": null,
  "circuitState": "...",
  "metrics": {...},
  "timestamp": "..."
}
```

**Action**: When Cursor prompts for approval, click "Approve"

#### Server 2: craft-server

**Tool**: `health_check`
**Location**: craft-server/src/server.ts (lines 712-717)
**Expected Response**:
```json
{
  "server": "craft-server",
  "version": "1.0.0",
  "craftRoot": "/home/caraxes/roots/python-craft",
  "rootExists": true,
  "pyprojectExists": true,
  "venvExists": true,
  "outDirExists": true,
  "uvVersion": "...",
  "moduleCount": 11,
  "renderCount": 8,
  "renderModules": [...]
}
```

**Action**: When Cursor prompts for approval, click "Approve"

#### Server 3: ori-server

**Tool**: `health_check`
**Location**: ori-server/src/server.ts (lines 83-113)
**Expected Response**:
```json
{
  "status": "ok",
  "s🔍 erver": "ori-server",
  "version": "1.0.0",
  "dataDir": "...",
  "logDir": "...",
  "todayLogEntries": 0,
  "totalLogEntries": 0,
  "riskPatterns": [...],
  "timestamp": "...",
  "circuitState": "...",
  "metrics": {...}
}
```

**Action**: When Cursor prompts for approval, click "Approve"

---

## Post-Approval Verification

### Step 1: Verify Approval in Cursor Config

```bash
# Check .cursor/mcp.json for approved servers
cat /home/caraxes/CascadeProjects/.cursor/mcp.json | grep -E "(harness|craft|ori)"
```

**Expected Output**: All three servers should appear in the approved list.

### Step 2: Test Server Invocation

From within the CascadeProjects workspace in Cursor, invoke each server's health_check tool again to verify they are now accessible without approval prompts.

### Step 3: Verify MCP Config Consistency

```bash
# Ensure canonical mcp_config.json matches Cursor's understanding
diff <(cat /home/caraxes/CascadeProjects/mcp_config.json | jq -r '.mcpServers | keys') \
     <(cat /home/caraxes/CascadeProjects/.cursor/mcp.json | jq -r 'keys')
```

**Expected Output**: No differences (or only expected editor-specific differences).

---

## Success Criteria

- [ ] All three servers appear in Cursor's MCP server list
- [ ] health_check can be invoked on each server without approval prompts
- [ ] health_check returns expected JSON responses
- [ ] No errors in Cursor's MCP server logs
- [ ] Servers are functional for their intended use cases

---

## Troubleshooting

### Issue: Server not found in Cursor MCP list

**Solution**:
1. Restart Cursor
2. Verify server configuration in mcp_config.json
3. Check Cursor's developer console for MCP errors

### Issue: health_check fails with error

**Solution**:
1. Check server logs in CascadeProjects/Tools/MCPServers/{server}/
2. Verify dependencies are installed (`npm install` in server directory)
3. Check environment variables are set correctly

### Issue: Approval dialog doesn't appear

**Solution**:
1. Ensure you're in the CascadeProjects workspace
2. Check Cursor's MCP settings are enabled
3. Try invoking a different MCP tool first to trigger the dialog

---

## Prevention Policy

### For New MCP Servers

1. **Configuration**: Add server to canonical `mcp_config.json`
2. **Installation**: Ensure dependencies are installed
3. **Verification**: Test server independently (`npm start` in server directory)
4. **Approval**: Open target workspace, invoke health_check, approve
5. **Documentation**: Update CHANGELOG.md with new server addition

### 🔁 Regular Maintenance

- Weekly: Verify all configured servers are approved in active workspaces
- Monthly: Review mcp_config.json for orphaned entries
- Quarterly: Audit server health and remove unused servers

---

## Documentation

Log approval actions to `/home/caraxes/.system-audit/mcp-approval-$(date +%Y%m%d-%H%M%S).log`:

```bash
cat > /home/caraxes/.system-audit/mcp-approval-$(date +%Y%m%d-%H%M%S).log << EOF
MCP Server Approval Log
Date: $(date)
Workspace: /home/caraxes/CascadeProjects

Servers Approved:
- harness-server: [APPROVED/PENDING/FAILED]
- craft-server: [APPROVED/PENDING/FAILED]
- ori-server: [APPROVED/PENDING/FAILED]

Notes:
[Add any issues or observations]
EOF
```

---

## Configuration Reference

### harness-server
```json
{
  "command": "npx",
  "args": ["-y", "tsx", "/home/caraxes/CascadeProjects/Tools/MCPServers/harness-server/src/server.ts"],
  "env": {
    "GATE_DIR": "/home/caraxes/CascadeProjects/Projects/GATE",
    "ECHOES_AUDIT_PATH": "/home/caraxes/.echoes/audit.ndjson",
    "GRID_API_URL": "http://localhost:8080"
  }
}
```

### craft-server
```json
{
  "command": "npx",
  "args": ["-y", "tsx", "/home/caraxes/CascadeProjects/Tools/MCPServers/craft-server/src/server.ts"],
  "env": {
    "CRAFT_ROOT": "/home/caraxes/roots/python-craft"
  }
}
```

### ori-server
```json
{
  "command": "npx",
  "args": ["-y", "tsx", "/home/caraxes/CascadeProjects/Tools/MCPServers/ori-server/src/server.ts"],
  "env": {
    "CASCADE_WORKSPACE_ROOT": "/home/caraxes/CascadeProjects",
    "ECHOES_AUDIT_PATH": "/home/caraxes/.echoes/audit.ndjson",
    "GRID_API_URL": "http://localhost:8080"
  }
}
```
