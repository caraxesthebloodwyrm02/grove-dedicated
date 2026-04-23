# GRID Mission Control - Structural Intelligence Implementation Guide

> **Version**: 1.0.0  
> **Status**: Design Complete | Implementation Ready  
> **Influences**: Continue.dev Mission Control, WakaTime, CodeScene, SonarQube Architecture as Code, Atmosphere Project

---

## Executive Summary

GRID Mission Control transforms the VS Code workspace into an **intelligent, self-aware interface** that provides developers with:

- 🌐 **Real-time System Status** - Health monitoring across all GRID components
- 📊 **Progress Tracking** - Productivity metrics, milestones, and burndown
- ⚠️ **Proactive Alerts** - Warnings, errors, and risk predictions
- 🗺️ **Strategic Roadmap** - Milestones, dependencies, and alliances
- 📜 **Activity Stream** - What's happening now and recent history

This document provides the implementation blueprint for building the structural intelligence layer.

---

## 1. Architecture Overview

### 1.1 System Diagram

```
┌─────────────────────────────────────────────────────────────────────────┐
│                        GRID MISSION CONTROL                              │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐   │
│  │   Status    │  │  Progress   │  │   Alerts    │  │  Roadmap    │   │
│  │   Panel     │  │   Panel     │  │   Panel     │  │   Panel     │   │
│  └──────┬──────┘  └──────┬──────┘  └──────┬──────┘  └──────┬──────┘   │
│         │                │                │                │           │
│  ┌──────┴────────────────┴────────────────┴────────────────┴──────┐   │
│  │                    Dashboard Controller                         │   │
│  └──────────────────────────┬──────────────────────────────────────┘   │
│                             │                                          │
│  ┌──────────────────────────┴──────────────────────────────────────┐   │
│  │                    Intelligence Engine                           │   │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐        │   │
│  │  │ Awareness│  │ Analysis │  │Prediction│  │  Action  │        │   │
│  │  │  Layer   │  │  Layer   │  │  Layer   │  │  Layer   │        │   │
│  │  └────┬─────┘  └────┬─────┘  └────┬─────┘  └────┬─────┘        │   │
│  └───────┴─────────────┴─────────────┴─────────────┴──────────────┘   │
│                             │                                          │
│  ┌──────────────────────────┴──────────────────────────────────────┐   │
│  │                    Data Integration Hub                          │   │
│  │  ┌────────────┐  ┌────────────┐  ┌────────────┐                 │   │
│  │  │  Internal  │  │  External  │  │   VS Code  │                 │   │
│  │  │  Sources   │  │  Sources   │  │    APIs    │                 │   │
│  │  └────────────┘  └────────────┘  └────────────┘                 │   │
│  └──────────────────────────────────────────────────────────────────┘   │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

### 1.2 Core Components

| Component | Responsibility | Key Classes |
|-----------|---------------|-------------|
| **Dashboard Controller** | UI rendering, user interaction | `DashboardController`, `PanelManager` |
| **Intelligence Engine** | Data processing, pattern recognition | `IntelligenceEngine`, `PatternAnalyzer` |
| **Data Integration Hub** | Data collection, normalization | `DataHub`, `SourceConnector` |
| **Event Bus** | Async event distribution | `EventBus`, `EventHandler` |
| **State Manager** | Persistent state, recovery | `StateManager`, `StateStore` |

---

## 2. Integration with Existing GRID Systems

### 2.1 Mothership Cockpit Integration

The Mission Control leverages the existing Mothership Cockpit infrastructure:

```python
# Integration with Mothership CockpitService
from application.mothership import CockpitService, CockpitState

class MissionControlBridge:
    """Bridge between Mission Control and Mothership Cockpit."""
    
    def __init__(self, cockpit: CockpitService):
        self.cockpit = cockpit
        self._register_event_handlers()
    
    def _register_event_handlers(self):
        """Register for cockpit events."""
        self.cockpit.add_event_handler(self._on_cockpit_event)
    
    def _on_cockpit_event(self, event: CockpitEvent):
        """Handle cockpit events and update Mission Control."""
        event_map = {
            "session_created": self._handle_session,
            "operation_completed": self._handle_operation,
            "component_health_changed": self._handle_health,
            "alert_created": self._handle_alert,
        }
        handler = event_map.get(event.event_type)
        if handler:
            handler(event)
    
    def get_health_summary(self) -> dict:
        """Get aggregated health from cockpit."""
        return self.cockpit.get_health_summary()
```

### 2.2 Integration Inbox Connection

Connect to the Integration Inbox for mismatch detection:

```python
# Integration with Integration Inbox
from AGENT.integration_inbox import IntegrationInbox, MismatchType

class IntegrationMonitor:
    """Monitor integration health and mismatches."""
    
    def __init__(self, inbox: IntegrationInbox):
        self.inbox = inbox
        self._mismatch_handlers = []
    
    def get_integration_status(self) -> list[dict]:
        """Get status of all integrations."""
        return [
            {
                "id": i.id,
                "name": i.name,
                "status": i.status.value,
                "health_score": self._calculate_health(i),
                "last_handshake": i.last_success_at,
                "error_count": i.error_count,
            }
            for i in self.inbox.integrations.values()
        ]
    
    def get_active_mismatches(self) -> list[dict]:
        """Get unresolved mismatches for alerts."""
        return self.inbox.get_daily_report()["resolution_queue"]
```

### 2.3 Master Workflow Guardrails

Connect to the Master Workflow for compliance monitoring:

```python
# Integration with Master Workflow
from pathlib import Path
import json

class GuardrailMonitor:
    """Monitor guardrail compliance."""
    
    RULES_PATH = Path(".windsurf/rules")
    SCHEMA_PATH = Path(".windsurf/grid-master-workflow-schema.json")
    INSTANCE_PATH = Path(".windsurf/grid-master-workflow-instance.json")
    
    def get_compliance_status(self) -> dict:
        """Get current guardrail compliance status."""
        return {
            "schema_valid": self._validate_schema(),
            "rules_count": len(list(self.RULES_PATH.glob("*.md"))),
            "violations": self._check_violations(),
            "last_check": datetime.now().isoformat(),
        }
    
    def _check_violations(self) -> list[dict]:
        """Check for guardrail violations."""
        violations = []
        # Check NON-CANONICAL headers in tooling files
        # Check citation format in canon files
        # Check exhibit manifest compliance
        return violations
```

---

## 3. Data Sources & Collection

### 3.1 Internal Sources

| Source | Module | Data Provided | Polling Interval |
|--------|--------|---------------|------------------|
| Mothership | `application.mothership` | Sessions, operations, health, alerts | 5s |
| Integration Inbox | `AGENT.integration_inbox` | Integrations, mismatches, EQ scores | 10s |
| Master Workflow | `.windsurf/workflows` | Guardrails, compliance | 30s |
| Circuits API | `circuits` | Decision engine, EQ processor | 15s |

### 3.2 VS Code API Sources

```typescript
// VS Code Extension Data Collection
import * as vscode from 'vscode';

class VSCodeDataCollector {
    // Diagnostics (errors, warnings)
    collectDiagnostics(): DiagnosticSummary {
        const diagnostics = vscode.languages.getDiagnostics();
        return {
            errors: diagnostics.filter(d => d[1].some(i => i.severity === 0)).length,
            warnings: diagnostics.filter(d => d[1].some(i => i.severity === 1)).length,
            hints: diagnostics.filter(d => d[1].some(i => i.severity === 3)).length,
        };
    }
    
    // Git status
    async collectGitStatus(): Promise<GitStatus> {
        const git = vscode.extensions.getExtension('vscode.git')?.exports;
        const repo = git?.getAPI(1)?.repositories[0];
        return {
            branch: repo?.state.HEAD?.name,
            ahead: repo?.state.HEAD?.ahead ?? 0,
            behind: repo?.state.HEAD?.behind ?? 0,
            changedFiles: repo?.state.workingTreeChanges.length ?? 0,
            stagedFiles: repo?.state.indexChanges.length ?? 0,
        };
    }
    
    // Task status
    collectTaskStatus(): TaskStatus[] {
        return vscode.tasks.taskExecutions.map(exec => ({
            name: exec.task.name,
            source: exec.task.source,
            isBackground: exec.task.isBackground,
        }));
    }
}
```

### 3.3 External Sources (Optional)

```python
# GitHub Integration (optional)
class GitHubConnector:
    """Connect to GitHub for issues, PRs, and actions."""
    
    def __init__(self, token: str, repo: str):
        self.token = token
        self.repo = repo
        self.base_url = f"https://api.github.com/repos/{repo}"
    
    async def get_open_issues(self) -> list[dict]:
        """Fetch open issues."""
        pass
    
    async def get_pr_status(self) -> list[dict]:
        """Fetch PR statuses."""
        pass
    
    async def get_workflow_runs(self) -> list[dict]:
        """Fetch GitHub Actions runs."""
        pass
```

---

## 4. Dashboard Implementation

### 4.1 Status Panel

```typescript
// Status Panel Webview
class StatusPanel {
    private _view: vscode.WebviewView;
    private _dataCollector: DataCollector;
    
    constructor(view: vscode.WebviewView, collector: DataCollector) {
        this._view = view;
        this._dataCollector = collector;
        this._startPolling();
    }
    
    private _startPolling() {
        setInterval(async () => {
            const status = await this._collectStatus();
            this._view.webview.postMessage({
                type: 'status-update',
                data: status
            });
        }, 5000);
    }
    
    private async _collectStatus(): Promise<SystemStatus> {
        return {
            health: await this._dataCollector.getSystemHealth(),
            sessions: await this._dataCollector.getActiveSessions(),
            operations: await this._dataCollector.getRunningOperations(),
            components: await this._dataCollector.getComponentHealth(),
        };
    }
    
    getHtml(): string {
        return `
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                .status-badge { 
                    display: inline-flex; 
                    align-items: center;
                    padding: 4px 12px;
                    border-radius: 16px;
                    font-weight: 600;
                }
                .status-healthy { background: #10B98120; color: #10B981; }
                .status-degraded { background: #FACC1520; color: #FACC15; }
                .status-critical { background: #EF444420; color: #EF4444; }
                
                .metric-card {
                    background: var(--vscode-editor-background);
                    border: 1px solid var(--vscode-widget-border);
                    border-radius: 8px;
                    padding: 16px;
                    margin: 8px 0;
                }
                
                .metric-value {
                    font-size: 24px;
                    font-weight: 700;
                    color: var(--vscode-foreground);
                }
                
                .metric-label {
                    font-size: 12px;
                    color: var(--vscode-descriptionForeground);
                }
            </style>
        </head>
        <body>
            <div id="status-container">
                <div class="status-header">
                    <span id="health-badge" class="status-badge status-healthy">
                        ● Healthy
                    </span>
                </div>
                
                <div class="metrics-grid">
                    <div class="metric-card">
                        <div class="metric-value" id="sessions-count">0</div>
                        <div class="metric-label">Active Sessions</div>
                    </div>
                    <div class="metric-card">
                        <div class="metric-value" id="operations-count">0</div>
                        <div class="metric-label">Running Operations</div>
                    </div>
                </div>
                
                <div id="component-health"></div>
            </div>
            
            <script>
                const vscode = acquireVsCodeApi();
                
                window.addEventListener('message', event => {
                    const { type, data } = event.data;
                    if (type === 'status-update') {
                        updateStatus(data);
                    }
                });
                
                function updateStatus(status) {
                    // Update health badge
                    const badge = document.getElementById('health-badge');
                    badge.className = 'status-badge status-' + status.health;
                    badge.textContent = '● ' + status.health.charAt(0).toUpperCase() + status.health.slice(1);
                    
                    // Update metrics
                    document.getElementById('sessions-count').textContent = status.sessions;
                    document.getElementById('operations-count').textContent = status.operations;
                }
            </script>
        </body>
        </html>
        `;
    }
}
```

### 4.2 Alerts Panel

```typescript
// Alert Management
interface Alert {
    id: string;
    severity: 'critical' | 'high' | 'medium' | 'low' | 'info';
    type: string;
    title: string;
    message: string;
    source: string;
    timestamp: Date;
    acknowledged: boolean;
    actions: AlertAction[];
}

class AlertsPanel {
    private _alerts: Map<string, Alert> = new Map();
    private _handlers: AlertHandler[] = [];
    
    addAlert(alert: Alert): void {
        this._alerts.set(alert.id, alert);
        this._notifyHandlers(alert);
        this._showNotification(alert);
    }
    
    private _showNotification(alert: Alert): void {
        if (alert.severity === 'critical' || alert.severity === 'high') {
            vscode.window.showErrorMessage(
                `🔴 ${alert.title}: ${alert.message}`,
                ...alert.actions.map(a => a.label)
            ).then(selected => {
                const action = alert.actions.find(a => a.label === selected);
                if (action) action.execute();
            });
        } else if (alert.severity === 'medium') {
            vscode.window.showWarningMessage(
                `🟡 ${alert.title}: ${alert.message}`
            );
        }
    }
    
    acknowledgeAlert(id: string): void {
        const alert = this._alerts.get(id);
        if (alert) {
            alert.acknowledged = true;
            this._updateUI();
        }
    }
    
    getAlertsSummary(): AlertSummary {
        const alerts = Array.from(this._alerts.values());
        return {
            critical: alerts.filter(a => a.severity === 'critical' && !a.acknowledged).length,
            high: alerts.filter(a => a.severity === 'high' && !a.acknowledged).length,
            medium: alerts.filter(a => a.severity === 'medium' && !a.acknowledged).length,
            low: alerts.filter(a => a.severity === 'low' && !a.acknowledged).length,
            total: alerts.filter(a => !a.acknowledged).length,
        };
    }
}
```

### 4.3 Progress Panel

```typescript
// Progress Tracking
interface ProgressMetrics {
    daily: {
        commits: number;
        testsPassed: number;
        testsRun: number;
        linesAdded: number;
        linesRemoved: number;
        filesChanged: number;
        activeTime: number; // minutes
    };
    sprint: {
        progress: number; // 0-100
        daysRemaining: number;
        completedTasks: number;
        totalTasks: number;
    };
    codeHealth: {
        score: number; // 1-10
        trend: 'improving' | 'stable' | 'declining';
        hotspots: string[];
    };
}

class ProgressTracker {
    private _metrics: ProgressMetrics;
    private _history: MetricSnapshot[] = [];
    
    async collectMetrics(): Promise<ProgressMetrics> {
        return {
            daily: await this._collectDailyMetrics(),
            sprint: await this._collectSprintMetrics(),
            codeHealth: await this._collectHealthMetrics(),
        };
    }
    
    private async _collectDailyMetrics(): Promise<ProgressMetrics['daily']> {
        // Collect from Git, WakaTime-style tracking, test runner
        const git = await this._getGitStats();
        const time = await this._getActiveTime();
        const tests = await this._getTestResults();
        
        return {
            commits: git.commits,
            linesAdded: git.additions,
            linesRemoved: git.deletions,
            filesChanged: git.files,
            testsPassed: tests.passed,
            testsRun: tests.total,
            activeTime: time.minutes,
        };
    }
    
    getProgressRing(): ProgressRingData {
        const metrics = this._metrics.daily;
        const goals = this._getDailyGoals();
        
        return {
            segments: [
                { label: 'Commits', value: metrics.commits, goal: goals.commits, color: '#3B82F6' },
                { label: 'Tests', value: metrics.testsPassed, goal: goals.tests, color: '#10B981' },
                { label: 'Time', value: metrics.activeTime, goal: goals.time, color: '#F97316' },
            ],
            overallProgress: this._calculateOverallProgress(metrics, goals),
        };
    }
}
```

---

## 5. Event System

### 5.1 Event Bus Implementation

```python
# Event Bus for Mission Control
from dataclasses import dataclass, field
from typing import Callable, Any
from datetime import datetime
from collections import defaultdict
import asyncio

@dataclass
class MissionControlEvent:
    """Event in the Mission Control system."""
    event_type: str
    source: str
    data: dict[str, Any]
    timestamp: datetime = field(default_factory=datetime.now)
    severity: str = "info"
    
    def to_dict(self) -> dict:
        return {
            "type": self.event_type,
            "source": self.source,
            "data": self.data,
            "timestamp": self.timestamp.isoformat(),
            "severity": self.severity,
        }

EventHandler = Callable[[MissionControlEvent], None]

class EventBus:
    """Central event bus for Mission Control."""
    
    def __init__(self):
        self._handlers: dict[str, list[EventHandler]] = defaultdict(list)
        self._queue: asyncio.Queue = asyncio.Queue()
        self._running = False
    
    def subscribe(self, event_type: str, handler: EventHandler) -> None:
        """Subscribe to events of a specific type."""
        self._handlers[event_type].append(handler)
    
    def subscribe_all(self, handler: EventHandler) -> None:
        """Subscribe to all events."""
        self._handlers["*"].append(handler)
    
    async def publish(self, event: MissionControlEvent) -> None:
        """Publish an event to all subscribers."""
        await self._queue.put(event)
    
    async def start(self) -> None:
        """Start processing events."""
        self._running = True
        while self._running:
            try:
                event = await asyncio.wait_for(self._queue.get(), timeout=1.0)
                await self._dispatch(event)
            except asyncio.TimeoutError:
                continue
    
    async def _dispatch(self, event: MissionControlEvent) -> None:
        """Dispatch event to handlers."""
        handlers = self._handlers.get(event.event_type, []) + self._handlers.get("*", [])
        for handler in handlers:
            try:
                if asyncio.iscoroutinefunction(handler):
                    await handler(event)
                else:
                    handler(event)
            except Exception as e:
                # Log but don't stop other handlers
                print(f"Event handler error: {e}")
```

### 5.2 Event Types

```python
# Predefined event types
class EventTypes:
    # System events
    SYSTEM_STARTED = "system.started"
    SYSTEM_STOPPED = "system.stopped"
    HEALTH_CHANGED = "system.health_changed"
    
    # Session events
    SESSION_CREATED = "session.created"
    SESSION_TERMINATED = "session.terminated"
    
    # Operation events
    OPERATION_STARTED = "operation.started"
    OPERATION_COMPLETED = "operation.completed"
    OPERATION_FAILED = "operation.failed"
    
    # Alert events
    ALERT_CREATED = "alert.created"
    ALERT_ACKNOWLEDGED = "alert.acknowledged"
    ALERT_RESOLVED = "alert.resolved"
    
    # Code events
    FILE_SAVED = "code.file_saved"
    DIAGNOSTIC_CHANGED = "code.diagnostic_changed"
    TEST_COMPLETED = "code.test_completed"
    
    # Git events
    COMMIT_CREATED = "git.commit_created"
    BRANCH_CHANGED = "git.branch_changed"
    PUSH_COMPLETED = "git.push_completed"
    
    # Integration events
    INTEGRATION_MISMATCH = "integration.mismatch"
    HANDSHAKE_FAILED = "integration.handshake_failed"
    
    # Workflow events
    GUARDRAIL_VIOLATION = "workflow.guardrail_violation"
    COMPLIANCE_CHECK = "workflow.compliance_check"
```

---

## 6. Status Bar Integration

```typescript
// Status Bar Item
class MissionControlStatusBar {
    private _statusBarItem: vscode.StatusBarItem;
    private _state: StatusBarState = {
        health: 'healthy',
        alertCount: 0,
        operationCount: 0,
    };
    
    constructor() {
        this._statusBarItem = vscode.window.createStatusBarItem(
            vscode.StatusBarAlignment.Right,
            100
        );
        this._statusBarItem.command = 'grid.openMissionControl';
        this._update();
        this._statusBarItem.show();
    }
    
    updateState(state: Partial<StatusBarState>): void {
        this._state = { ...this._state, ...state };
        this._update();
    }
    
    private _update(): void {
        const { health, alertCount, operationCount } = this._state;
        
        // Build status text
        const healthIcon = {
            healthy: '$(check)',
            degraded: '$(warning)',
            critical: '$(error)',
            offline: '$(circle-slash)',
        }[health];
        
        let text = `${healthIcon} GRID`;
        
        if (alertCount > 0) {
            text += ` $(bell-dot) ${alertCount}`;
        }
        
        if (operationCount > 0) {
            text += ` $(sync~spin) ${operationCount}`;
        }
        
        this._statusBarItem.text = text;
        
        // Set color based on health
        this._statusBarItem.backgroundColor = health === 'critical' 
            ? new vscode.ThemeColor('statusBarItem.errorBackground')
            : health === 'degraded'
            ? new vscode.ThemeColor('statusBarItem.warningBackground')
            : undefined;
        
        // Set tooltip
        this._statusBarItem.tooltip = this._buildTooltip();
    }
    
    private _buildTooltip(): vscode.MarkdownString {
        const md = new vscode.MarkdownString();
        md.appendMarkdown('### GRID Mission Control\n\n');
        md.appendMarkdown(`**Health:** ${this._state.health}\n\n`);
        md.appendMarkdown(`**Alerts:** ${this._state.alertCount}\n\n`);
        md.appendMarkdown(`**Operations:** ${this._state.operationCount}\n\n`);
        md.appendMarkdown('---\n\n');
        md.appendMarkdown('$(link-external) Click to open dashboard');
        md.isTrusted = true;
        return md;
    }
}
```

---

## 7. VS Code Extension Entry Point

```typescript
// extension.ts - Main entry point
import * as vscode from 'vscode';

let missionControl: MissionControl | undefined;

export function activate(context: vscode.ExtensionContext) {
    console.log('GRID Mission Control activating...');
    
    // Initialize Mission Control
    missionControl = new MissionControl(context);
    
    // Register commands
    context.subscriptions.push(
        vscode.commands.registerCommand('grid.openMissionControl', () => {
            missionControl?.showDashboard();
        }),
        vscode.commands.registerCommand('grid.showAlerts', () => {
            missionControl?.showAlertsPanel();
        }),
        vscode.commands.registerCommand('grid.acknowledgeAlert', (alertId: string) => {
            missionControl?.acknowledgeAlert(alertId);
        }),
        vscode.commands.registerCommand('grid.refreshStatus', () => {
            missionControl?.refresh();
        }),
    );
    
    // Register tree view providers
    context.subscriptions.push(
        vscode.window.registerTreeDataProvider(
            'grid.statusTree',
            missionControl.statusTreeProvider
        )
    );
    
    // Register webview providers
    context.subscriptions.push(
        vscode.window.registerWebviewViewProvider(
            'grid.missionControlPanel',
            missionControl.panelProvider
        )
    );
    
    // Start Mission Control
    missionControl.start();
    
    console.log('GRID Mission Control activated');
}

export function deactivate() {
    missionControl?.stop();
    missionControl = undefined;
}

class MissionControl {
    private _context: vscode.ExtensionContext;
    private _statusBar: MissionControlStatusBar;
    private _eventBus: EventBus;
    private _dataHub: DataHub;
    private _alertManager: AlertsPanel;
    private _progressTracker: ProgressTracker;
    
    public statusTreeProvider: StatusTreeProvider;
    public panelProvider: MissionControlPanelProvider;
    
    constructor(context: vscode.ExtensionContext) {
        this._context = context;
        this._statusBar = new MissionControlStatusBar();
        this._eventBus = new EventBus();
        this._dataHub = new DataHub();
        this._alertManager = new AlertsPanel();
        this._progressTracker = new ProgressTracker();
        
        this.statusTreeProvider = new StatusTreeProvider(this._dataHub);
        this.panelProvider = new MissionControlPanelProvider(
            context.extensionUri,
            this._dataHub,
            this._alertManager
        );
        
        this._setupEventHandlers();
    }
    
    private _setupEventHandlers(): void {
        // Update status bar on events
        this._eventBus.subscribeAll((event) => {
            if (event.event_type.startsWith('alert.')) {
                this._statusBar.updateState({
                    alertCount: this._alertManager.getAlertsSummary().total
                });
            }
            if (event.event_type === 'system.health_changed') {
                this._statusBar.updateState({
                    health: event.data.health
                });
            }
        });
    }
    
    async start(): Promise<void> {
        await this._dataHub.connect();
        this._eventBus.start();
        await this.refresh();
    }
    
    async stop(): Promise<void> {
        await this._dataHub.disconnect();
    }
    
    async refresh(): Promise<void> {
        const status = await this._dataHub.collectAll();
        this._statusBar.updateState(status);
        this.statusTreeProvider.refresh();
    }
    
    showDashboard(): void {
        vscode.commands.executeCommand('workbench.view.extension.grid-mission-control');
    }
    
    showAlertsPanel(): void {
        vscode.commands.executeCommand('grid.missionControlPanel.focus');
    }
    
    acknowledgeAlert(alertId: string): void {
        this._alertManager.acknowledgeAlert(alertId);
    }
}
```

---

## 8. Configuration Schema

Add to `package.json` for VS Code extension:

```json
{
  "contributes": {
    "viewsContainers": {
      "activitybar": [
        {
          "id": "grid-mission-control",
          "title": "GRID Mission Control",
          "icon": "$(dashboard)"
        }
      ]
    },
    "views": {
      "grid-mission-control": [
        {
          "type": "webview",
          "id": "grid.missionControlPanel",
          "name": "Dashboard"
        },
        {
          "id": "grid.statusTree",
          "name": "Status"
        },
        {
          "id": "grid.alertsTree",
          "name": "Alerts"
        }
      ]
    },
    "commands": [
      {
        "command": "grid.openMissionControl",
        "title": "Open Mission Control",
        "category": "GRID",
        "icon": "$(dashboard)"
      },
      {
        "command": "grid.refreshStatus",
        "title": "Refresh Status",
        "category": "GRID",
        "icon": "$(refresh)"
      },
      {
        "command": "grid.showAlerts",
        "title": "Show Alerts",
        "category": "GRID",
        "icon": "$(bell)"
      }
    ],