---
description: Commands that should NEVER be auto-run (SafeToAutoRun must be false)
---

# Command Denylist

Commands matching these patterns should require user approval.

## File/Directory Modification
- `mv`, `move`, `Move-Item` - move files/directories
- `rm`, `del`, `Remove-Item` - delete files/directories  
- `mkdir`, `New-Item -ItemType Directory` - create directories
- `cp`, `copy`, `Copy-Item` - copy files (can overwrite)
- `rename`, `Rename-Item` - rename files

## Git Operations (State-Changing)
- `git checkout` - can discard changes
- `git reset` - can lose commits
- `git clean` - deletes untracked files
- `git push` - publishes to remote
- `git merge` - merges branches
- `git rebase` - rewrites history
- `git stash drop` - loses stashed changes

## Package/System
- `pip install`, `pip uninstall` - modifies packages
- `npm install`, `npm uninstall` - modifies packages
- Any command with `--force`, `-f`, `-rf`

## Safe to Auto-Run (allowlist)
- `dir`, `ls`, `Get-ChildItem` - list files
- `cat`, `type`, `Get-Content` - read files
- `pwd`, `Get-Location` - current directory
- `python -c "..."` for read-only operations
- `git status`, `git log`, `git diff` - read-only git
- `echo`, `Write-Output` - display text
