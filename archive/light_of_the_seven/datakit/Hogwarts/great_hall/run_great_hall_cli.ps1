<#
.SYNOPSIS
    Runs the Great Hall recommended stream runner to generate discussion tables and receipts.

.DESCRIPTION
    This script wraps 'run_recommended_stream.py' to ensure a robust execution environment.
    It detects Python, supports isolated mode to prevent environment poisoning, and
    generates the 'discussion_table.csv' and 'receipt.json' artifacts.

.PARAMETER PythonPath
    Optional path to the Python executable. Defaults to 'py' (launcher) or 'python' found in PATH.

.PARAMETER Isolated
    Forces Python to run in isolated mode (-I) to ignore PYTHONPATH/PYTHONHOME.
    Defaults to $true to prevent common 'encodings module not found' errors in complex environments.

.EXAMPLE
    .\run_great_hall_cli.ps1 -Verbose

    Description: Runs the runner using default python detection in isolated mode.

.NOTES
    Version: 1.0
    Author: Great Hall Scribe
    Date: 2025-12-14
#>
[CmdletBinding(
    SupportsShouldProcess=$true,
    ConfirmImpact='Medium'
)]
param(
    [Parameter(Position=0,
               HelpMessage='Path to python executable.')]
    [string]$PythonPath,

    [switch]$Isolated = $true
)

#---------------------------------------------------
# BEGIN Block: Setup and Initialization
#---------------------------------------------------
begin {
    Write-Verbose "Starting script execution at $(Get-Date)"

    $ErrorActionPreference = 'Stop'

    # Define target script relative to this script
    $TargetScript = Join-Path -Path $PSScriptRoot -ChildPath "run_recommended_stream.py"

    if (-not (Test-Path $TargetScript)) {
        Throw "Target script not found: $TargetScript"
    }

    # Auto-detect Python if not provided
    if ([string]::IsNullOrWhiteSpace($PythonPath)) {
        if (Get-Command "py" -ErrorAction SilentlyContinue) {
            $PythonPath = "py"
            Write-Verbose "Auto-detected Python Launcher: py"
        } elseif (Get-Command "python" -ErrorAction SilentlyContinue) {
            $PythonPath = "python"
            Write-Verbose "Auto-detected Python: python"
        } else {
            Throw "No python executable found in PATH. Please specify -PythonPath."
        }
    }
}

#---------------------------------------------------
# PROCESS Block: Main Logic
#---------------------------------------------------
process {
    Write-Verbose "Processing target script: $TargetScript"

    try {
        if ($PSCmdlet.ShouldProcess($TargetScript, "Run Great Hall Table Builder")) {

            Write-Host "Starting Great Hall Table Builder..." -ForegroundColor Cyan

            $ProcArgs = @()

            # Handle Isolation and Launcher arguments
            if ($Isolated) {
                if ($PythonPath -eq "py") {
                     # Request Python 3 explicit
                    $ProcArgs += "-3"
                }
                $ProcArgs += "-I"
            }

            $ProcArgs += $TargetScript

            Write-Verbose "Executing: $PythonPath $ProcArgs"

            # Execute using call operator to preserve stream output in current console
            & $PythonPath $ProcArgs

            if ($LASTEXITCODE -eq 0) {
                Write-Host "Task completed successfully." -ForegroundColor Green

                # Check for expected outputs
                $OutDir = Join-Path $PSScriptRoot "outputs"
                if (Test-Path $OutDir) {
                    Get-ChildItem $OutDir | ForEach-Object {
                        Write-Host "Generated: $($_.Name)" -ForegroundColor Gray
                    }
                }
            } else {
                Write-Error "Table builder failed with exit code $LASTEXITCODE."
            }
        }
    }
    catch {
        Write-Error "An error occurred during execution: $($_.Exception.Message)"
    }
}

#---------------------------------------------------
# END Block: Cleanup and Finalization
#---------------------------------------------------
end {
    Write-Verbose "Script execution finished."
}
