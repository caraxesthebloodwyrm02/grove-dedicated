#!/usr/bin/env bash
# install hooks into .git/hooks (PoC)
set -e
HOOK_DEST=.git/hooks
mkdir -p "$HOOK_DEST"
cp scripts/hooks/commit-msg "$HOOK_DEST/commit-msg"
chmod +x "$HOOK_DEST/commit-msg"
echo "Installed commit-msg hook."
