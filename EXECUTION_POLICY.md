# System Execution Policy

> Structured execution protocols for maintaining system health, workspace hygiene, and MCP infrastructure integrity based on audit findings.

**Based on Audit Findings — April 15, 2026**
**Scope: Workspace Management, System Performance, MCP Infrastructure**

---

## Table of Contents

1. [Policy Overview](#policy-overview)
2. [Policy Classification](#policy-classification)
3. [Current Audit Findings & Remediation](#current-audit-findings--remediation)
4. [Ongoing Maintenance Policy](#ongoing-maintenance-policy)
5. [Execution Protocol](#execution-protocol)
6. [Escalation Matrix](#escalation-matrix)
7. [Change Management](#change-management)
8. [Compliance & Audit Trail](#compliance--audit-trail)

---

## Policy Overview

This policy defines structured execution protocols for maintaining system health, workspace hygiene, and MCP infrastructure integrity. It addresses critical findings from the system audit and establishes ongoing maintenance procedures.

---

## Policy Classification

### P0 — Critical (Immediate Action Required)
- System stability threats
- Security vulnerabilities
- Data loss risks

### P1 — High (Within 24 Hours)
- Performance degradation
- Resource exhaustion
- Infrastructure blocking issues

### P2 — Medium (Within 7 Days)
- Workspace hygiene
- Configuration optimization
- Documentation gaps

### P3 — Low (Advisory)
- Nice-to-have improvements
- Future-proofing measures

---

## Current Audit Findings & Remediation

### 🔴 Finding 1: Critical CPU Overload (P0)

**Issue**: Multiple `fscrypt unlock` processes stuck in abnormal state consuming 1200%+ CPU

| Metric | Value | Status |
|--------|-------|--------|
| Load Average | 31.68, 33.51, 33.43 | 🔴 Critical (2× CPU core count) |
| Affected Processes | 5+ at 254% CPU each | 🔴 Abnormal |
| System State | Severely overloaded | 🔴 Degraded |

**Root Cause Analysis Required**:
- Why are fscrypt processes hanging?
- Which encrypted directories are affected?
- Is this a filesystem corruption or encryption key issue?

**Remediation Exercise**:
```bash
# Step 1: Identify hung processes
ps aux | grep fscrypt

# Step 2: Terminate stuck processes (CAUTION: may affect encrypted access)
pkill -9 fscrypt

# Step 3: Verify system recovery
watch -n 1 'uptime'

# Step 4: Investigate root cause
journalctl -xe | grep -i fscrypt
ls -la /home/caraxes/.config/chromium  # Check encrypted directory status

# Step 5: Test encrypted access after remediation
# Attempt to access encrypted directories to verify functionality
```

**Prevention Policy**:
- Monitor fscrypt process count and CPU usage daily
- Set up alert for load average > 20
- Review encrypted directory health weekly

---

* harness-server
- craft-server
 ori

**Impact**: Servers cannot be invoked from CascadeProjects workspace in Curs

**Remediation Exercise**:
1. Open `/home/caraxes/CascadeProjects` workspace in Cursor
2. For each server, invoke `health_check` tool:
   - harness-server: health_check (line 55-87 in server.ts)
   - craft-server: health_check (line 712-717 in server.ts)
   - ori-server: health_check (line 83-113 in server.ts)
3. Approve servers when prompted by Cursor

**Verification**:
```bash
# Check that servers are approved in .cursor/mcp.json
cat /home/caraxes/CascadeProjects/.cursor/mcp.json | grep -E "(harness|craft|ori)"
```

**Prevention Policy**:
- All new MCP servers must be approved within 24 hours of configuration
- Update mcp_config.json canonical source immediately after adding servers
- Verify approval in target editor before considering deployment complete

---

### 🟢 Finding 3: Duplicate Configuration Pattern (P2)

**Issue**: Byte-identical `.cursor/settings.json` in 2 canopy repos

| Repository | Path | Size | Plugins |
|------------|------|------|---------|
| canopy/afloat | .cursor/settings.json | 124 bytes | huggingface-skills, vercel |
| canopy/assistive-agreement-contracts | .cursor/settings.json | 124 bytes | huggingface-skills, vercel |

**Current Status**: Below threshold (3+ repos) for symlinking recommendation — monitor for pattern spread.

**Monitoring Policy**:
- Track duplicate settings.json across canopy repos
- If pattern spreads to 3+ repos, create shared template:
  ```bash
  # Proposed structure
  /home/caraxes/canopy/.cursor-template/settings.json
  /home/caraxes/canopy/afloat/.cursor/settings.json -> ../../.cursor-template/settings.json
  /home/caraxes/canopy/assistive-agreement-contracts/.cursor/settings.json -> ../../.cursor-template/settings.json
  ```

---

## Ongoing Maintenance Policy

### Daily Checks (Automated)

```bash
#!/bin/bash
# daily_system_check.sh

# Check load average
LOAD=$(uptime | awk -F'load average:' '{print $2}' | awk '{print $1}' | sed 's/,//')
if (( $(echo "$LOAD > 20" | bc -l) )); then
  echo "CRITICAL: Load average $LOAD exceeds threshold"
  # Send alert
fi

# Check for stuck fscrypt processes
FSCRYPT_COUNT=$(ps aux | grep fscrypt | grep -v grep | wc -l)
if [ $FSCRYPT_COUNT -gt 2 ]; then
  echo "WARNING: $FSCRYPT_COUNT fscrypt processes running"
fi

# Check disk usage
DISK_USAGE=$(df /home/caraxes | tail -1 | awk '{print $5}' | sed 's/%//')
if [ $DISK_USAGE -gt 80 ]; then
  echo "WARNING: Disk usage at $DISK_USAGE%"
fi

# Check memory pressure
MEM_AVAILABLE=$(free -m | awk 'NR==2{printf "%.0f", $7}')
if [ $MEM_AVAILABLE -lt 2048 ]; then
  echo "WARNING: Low memory available (${MEM_AVAILABLE}MB)"
fi
```

### Weekly Maintenance

1. **Workspace Cleanup**
   - Scan for tmp-* directories older than 7 days
   - Remove stale backup files (*.bak-*)
   - Verify MCP config consistency

2. **MCP Infrastructure**
   - Verify all configured servers are approved
   - Check server health via health_check tools
   - Review mcp_config.json for orphaned entries

3. **System Health**
   - Review system logs for anomalies
   - Check for hung processes
   - Verify encrypted directory integrity

### Monthly Review

1. **Workspace Distribution Analysis**
   - Measure storage footprint per workspace
   - Identify growth trends
   - Plan capacity adjustments

2. **Performance Baseline Update**
   - Record typical load averages
   - Document memory usage patterns
   - Update alert thresholds if needed

3. **Configuration Audit**
   - Review duplicate configuration patterns
   - Consolidate where appropriate
   - Update documentation

---

## Execution Protocol

### P0 Issues (Critical)
1. Immediate containment
2. Root cause investigation within 1 hour
3. Remediation within 4 hours
4. Post-incident review within 24 hours

### P1 Issues (High)
1. Assessment within 2 hours
2. Remediation within 24 hours
3. Verification within 48 hours

### P2 Issues (Medium)
1. Assessment within 1 week
2. Remediation within 2 weeks
3. Documentation update

### P3 Issues (Low)
1. Backlog prioritization
2. Address during scheduled maintenance windows
3. No strict timeline

---

## Escalation Matrix

| Severity | Response Time | Escalation Path |
|----------|---------------|-----------------|
| P0 | < 15 min | Immediate → System Administrator |
| P1 | < 2 hours | → Development Lead → System Administrator |
| P2 | < 24 hours | → Development Lead |
| P3 | Next maintenance window | → Development Lead |

---

## Change Management

### Configuration Changes
1. Update canonical source (mcp_config.json)
2. Propagate to editor-specific configs
3. Verify in all target environments
4. Document change in CHANGELOG.md

### Workspace Changes
1. Impact assessment
2. Backup critical data
3. Execute change
4. Verify functionality
5. Update documentation

---

## Compliance & Audit Trail

All remediation actions must be documented with:
- Timestamp
- Action taken
- Rationale
- Outcome
- Verification steps

Audit log location: `/home/caraxes/.system-audit/`

---

## Policy Version

**Version**: 1.0
**Effective**: April 15, 2026
**Review Date**: May 15, 2026
**Owner**: System Administrator
**Approved By**: Development Lead
**Review Date**: May 15, 2026
**Owner**: System Administrator
**Approved By**: Development Lead
**Review Date**: May 15, 2026
**Owner**: System Administrator
**Approved By**: Development Lead
