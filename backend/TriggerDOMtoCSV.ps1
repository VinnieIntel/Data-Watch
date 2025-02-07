# Define the path to the Python executable
$pythonPath = "C:\Users\vtiang\AppData\Local\Programs\Python\Python310\python.exe"

# Define the path to the Python script
$scriptPath = "C:\Projects\datawatchUI\backend\DOMtoCSV.py"

# Run the Python script
& $pythonPath $scriptPath

# Optional: Log the execution
$logPath = "C:\Projects\DataWatchUI\backend\logfiles\ps_script_log.txt"
Add-Content -Path $logPath -Value "$(Get-Date): DOMtoCSV.py executed."
