# perf/run_sweep.ps1
# Powershell runner with SIMULATE mode
param(
  [switch]$Simulate
)

$OutDir = "perf\results"
$LogDir = "perf\logs"
$PidDir = "perf\pids"
New-Item -ItemType Directory -Force -Path $OutDir, $LogDir, $PidDir | Out-Null

$AllCsv = "$OutDir\all_runs.csv"
if (-not (Test-Path $AllCsv)) {
  "run_id,build_mode,concurrency,input_size,repeat,duration_s,throughput_rps,p50_ms,p95_ms,p99_ms,error_rate,cpu_pct,rss_kb,notes,timestamp" | Out-File -FilePath $AllCsv -Encoding utf8
}

$ServerCmdDefault = ".\target\release\magical_forest.exe"
$Endpoint = "http://127.0.0.1:8080/"
$Duration = 30
$Repeats = 5
$Concurrencies = @(1,4,8,16)
$InputSizes = @("small","medium","large")
$Builds = @("release","release-lto")

function Timestamp { Get-Date -Format o }

foreach ($build in $Builds) {
  Write-Host "--- build: $build"
  if ($Simulate) { Write-Host "SIMULATE: build $build" }
  else {
    if ($build -eq 'release') { Write-Host 'cargo build --release'; cargo build --release }
    else { Write-Host 'RUSTFLAGS="-C lto -C codegen-units=1" cargo build --release'; $env:RUSTFLAGS='-C lto -C codegen-units=1'; cargo build --release; Remove-Item Env:RUSTFLAGS }
  }

  foreach ($input_size in $InputSizes) {
    foreach ($c in $Concurrencies) {
      for ($rep=1; $rep -le $Repeats; $rep++) {
        $run_id = "${build}_${input_size}_c${c}_r${rep}_$(Get-Date -UFormat %s)"
        Write-Host "== run: $run_id =="

        if ($Simulate) {
          $seed = (($c * $rep) + $input_size.Length)
          $throughput = 1000 + ($seed % 500)
          $p50 = [math]::Round(10 + ($seed % 10), 1)
          $p95 = [math]::Round(40 + ($seed % 20), 1)
          $p99 = [math]::Round(80 + ($seed % 30), 1)
          $cpu = [math]::Round(20 + ($seed % 50), 1)
          $rss = 20000 + ($seed * 100)
          $ts = Timestamp
          "$run_id,$build,$c,$input_size,$rep,$Duration,$throughput,$p50,$p95,$p99,0.00,$cpu,$rss,simulated,$ts" | Out-File -FilePath $AllCsv -Append -Encoding utf8
          continue
        }

        $ServerCmd = $env:SERVER_CMD
        if (-not $ServerCmd) { $ServerCmd = $ServerCmdDefault }
        Write-Host "Starting server: $ServerCmd"
        $proc = Start-Process -FilePath $ServerCmd -NoNewWindow -PassThru -RedirectStandardOutput "$LogDir\server-${run_id}.log" -RedirectStandardError "$LogDir\server-${run_id}.err"
        $proc.Id | Out-File -FilePath "$PidDir\${run_id}.pid" -Encoding utf8

        Start-Sleep -Seconds 1

        Write-Host "Running load: wrk -t2 -c$c -d${Duration}s $Endpoint"
        $wrkOut = & wrk -t2 -c$c -d$Duration`s $Endpoint 2>&1

        $throughput = ($wrkOut | Select-String 'Requests/sec').ToString().Split(':')[1].Trim()

        $stats = Get-Process -Id $proc.Id | Select-Object CPU,WorkingSet
        $cpuPct = $stats.CPU
        $rssKb = [int]($stats.WorkingSet / 1KB)

        $ts = Timestamp
        "$run_id,$build,$c,$input_size,$rep,$Duration,$throughput,0,0,0,0.00,$cpuPct,$rssKb,ok,$ts" | Out-File -FilePath $AllCsv -Append -Encoding utf8

        Write-Host "Stopping server pid $($proc.Id)"
        Stop-Process -Id $proc.Id -Force -ErrorAction SilentlyContinue
      }
    }
  }
}

Write-Host "All runs appended to $AllCsv"
Write-Host "Done. To run in simulate mode: .\perf\run_sweep.ps1 -Simulate"
