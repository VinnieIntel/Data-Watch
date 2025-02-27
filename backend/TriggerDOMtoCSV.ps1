# TriggerDOMtoCSV.ps1

# Define paths
$pythonPath = "C:\VinnieProjects\Data-Watch\backend\venv\Scripts\python.exe"
$domScriptPath = "C:\VinnieProjects\Data-Watch\backend\DOMtoCSV.py"
$logPath = "C:\VinnieProjects\Data-Watch\backend\data\logfiles\ps_script_DOMtoCSV.log"

# Function to write to log
function Write-Log($message) {
    Add-Content -Path $logPath -Value "$(Get-Date): $message"
}

# Check if DOMtoCSV.py is already running by filtering python processes that contain "DOMtoCSV.py" in the command line
$existingProcess = Get-CimInstance Win32_Process -Filter "Name = 'python.exe'" | Where-Object { $_.CommandLine -match "DOMtoCSV.py" }

if (-not $existingProcess) {
    # Start DOMtoCSV.py in the background (hidden window)
    Start-Process -FilePath $pythonPath -ArgumentList $domScriptPath -WindowStyle Hidden
    Write-Log "DOMtoCSV.py triggered."
} else {
    Write-Log "DOMtoCSV.py is already running."
}
