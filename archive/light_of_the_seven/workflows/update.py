"""Wrapper for workflow update PowerShell script."""

import subprocess
import sys
from pathlib import Path

def update_daily_files() -> None:
    """Run the workflow update PowerShell script."""
    script_path = Path(__file__).parent / "update.ps1"

    # Determine command based on platform
    if sys.platform == "win32":
        cmd = ["powershell", "-ExecutionPolicy", "Bypass", "-File", str(script_path)]
    else:
        # On WSL/Linux, use pwsh if available, otherwise try powershell.exe
        # This assumes powershell is available in the path
        import shutil
        if shutil.which("pwsh"):
            cmd = ["pwsh", "-File", str(script_path)]
        else:
            # Fallback to calling Windows PowerShell from WSL
            cmd = ["powershell.exe", "-ExecutionPolicy", "Bypass", "-File", str(script_path)]

    subprocess.run(cmd, check=True)
