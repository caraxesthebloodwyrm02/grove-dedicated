---
description: GRID Git Manager Onboarding Workflow
---

# GRID Git Manager Onboarding

This workflow guides you through initializing and validating your Git environment for the GRID workspace.

## Step 1: Initialize the Manager
Ensure you have the `git_manager.py` script available in your `scripts/` directory.

## Step 2: Audit Current State
Run the status command to see your current Git identity and local configuration.
```bash
python scripts/git_manager.py status
```

## Step 3: Repair Misconfigurations
If the status command reveals mismatches (e.g., incorrect default branch or line ending settings), run the repair command.
```bash
python scripts/git_manager.py repair
```

## Step 4: Locomote to a Platform
To start working on a specific platform integration, use the locomotion command to switch context and see available actions.
```bash
python scripts/git_manager.py locomote <platform_id>
```

## Step 5: Start a Topic Branch
Use the integrated topic management to create a new branch following GRID conventions.
```bash
python scripts/git_manager.py topic create --theme <theme> --short <description>
```
