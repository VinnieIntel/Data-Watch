$pythonPath = "C:\VinnieProjects\Data-Watch\backend\venv\Scripts\python.exe"
$scriptPath = "C:\VinnieProjects\Data-Watch\backend\ToolStatusFull.py"
$logPath = "C:\VinnieProjects\Data-Watch\backend\data\logfiles\ps_script_toolstatus.log"

Start-Process -FilePath $pythonPath -ArgumentList $scriptPath -WindowStyle Hidden

# Optional: Log the execution
Add-Content -Path $logPath -Value "$(Get-Date): ToolStatusFull.py executed."