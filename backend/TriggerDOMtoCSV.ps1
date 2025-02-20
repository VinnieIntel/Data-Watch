$pythonPath = "C:\VinnieProjects\Data-Watch\backend\venv\Scripts\python.exe"


$script1 = "C:\VinnieProjects\Data-Watch\backend\DOMtoCSV.py"
# $script2 = "C:\VinnieProjects\Data-Watch\backend\ToolStatusFull.py"
$logPath = "C:\VinnieProjects\Data-Watch\backend\data\logfiles\ps_script.log"
Add-Content -Path $logPath -Value "$(Get-Date): This is the logging from ps1."

# Run the Python script
# & $pythonPath $script1
Start-Process -FilePath $pythonPath -ArgumentList $script1 -WindowStyle Hidden
Add-Content -Path $logPath -Value "$(Get-Date): DOMtoCSV.py executed."


Add-Content -Path $logPath -Value "$(Get-Date) : TriggerDOMtoCSV.ps1 finished"