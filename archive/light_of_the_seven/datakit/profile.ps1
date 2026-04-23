function Set-GridRepo {
  Set-Location "E:\grid\light_of_the_seven\full_datakit"
}

function Set-GridInterpreter {
  param(
    [string]$PythonExe = "E:\grid\light_of_the_seven\full_datakit\.venv\Scripts\python.exe"
  )
  $env:INTERPRETERPATH = $PythonExe
  & $env:INTERPRETERPATH --version
}

function Use-GridVenv {
  $venvActivate = "E:\grid\light_of_the_seven\full_datakit\.venv\Scripts\Activate.ps1"
  if (Test-Path $venvActivate) {
    . $venvActivate
    $env:INTERPRETERPATH = (Resolve-Path "E:\grid\light_of_the_seven\full_datakit\.venv\Scripts\python.exe").Path
  } else {
    Write-Host "Venv not found. Create it: python -m venv .venv" -ForegroundColor Yellow
  }
}

function Run-GreatHall {
  $script = "E:\grid\light_of_the_seven\full_datakit\visualizations\Hogwarts\great_hall\run_great_hall_cli.ps1"
  if (!(Test-Path $script)) { throw "Missing: $script" }
  if (![string]::IsNullOrWhiteSpace($env:INTERPRETERPATH)) {
    & $script -PythonPath $env:INTERPRETERPATH -Verbose
  } else {
    & $script -Verbose
  }
}