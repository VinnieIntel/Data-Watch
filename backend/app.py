from flask import Flask, jsonify, send_from_directory
from flask_cors import CORS
import os
import csv
import re
import subprocess

app = Flask(__name__)
CORS(app)  # Enable CORS to allow React to access the API
@app.route('/')
def home():
    return "Hello, This is the backend of Data Watch! :)"

script_dir = os.path.dirname(__file__)

############################### BACKEND TRIGGER ####################################
# ps1_script = os.path.join(script_dir, "TriggerDOMtoCSV.ps1")
# print("This is the output from app.py")
# print(ps1_script)

# log_file = os.path.join(script_dir, "data","logfiles","script_output.log")
# log_dir = os.path.dirname(log_file)
# os.makedirs(log_dir, exist_ok=True)

# with open(log_file, "w") as log:
#     print("This logs the run of ps1 to call DOMtoCSV.py from app.py")
#     process = subprocess.Popen(
#         ["powershell.exe", "-ExecutionPolicy", "Bypass", "-File", ps1_script],
#         stdout=log, stderr=log
#     )


############################### HOME ####################################
# Path to the CSV file
DATA_PATH = os.path.join(os.path.dirname(__file__), 'data', 'Trigger_Data_TEST.csv')

# Route to fetch CSV data
@app.route('/api/csv', methods=['GET'])
def get_csv_data():
    try:
        # Read CSV and convert to a list of dictionaries
        with open(DATA_PATH, 'r') as csvfile:
            reader = csv.DictReader(csvfile)
            fieldnames = reader.fieldnames
            data = list(reader)[:20]  # Convert the CSV rows to a list of dictionaries
        return jsonify({"columns": fieldnames, "data": data})  # Return as JSON response
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Define the path to the backend folder containing the full csv file
BACKEND_FOLDER = os.path.join(os.getcwd(), 'data')
print(BACKEND_FOLDER)
# Route to serve RuleCreation.py for download
@app.route('/api/download/full-csv', methods=['GET'])
def download_full_csv():
    try:
        # Check if the file exists
        file_name = "output_2.csv"
        file_path = os.path.join(BACKEND_FOLDER, file_name)
        if not os.path.exists(file_path):
            return jsonify({"error": "File not found"}), 404
        
        # Serve the file
        return send_from_directory(BACKEND_FOLDER, file_name, as_attachment=True)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    


############################### STATUS ####################################
# Path to the CSV file
STATUS_PATH = os.path.join(os.path.dirname(__file__), 'data', 'toolstatus_show.csv')

# Route to fetch status data
@app.route('/api/status', methods=['GET'])
def get_status_data():
    try:
        # Read CSV and convert to a list of dictionaries
        with open(STATUS_PATH, 'r') as csvfile:
            reader = csv.DictReader(csvfile)
            fieldnames = reader.fieldnames
            data = list(reader)
        return jsonify({"columns": fieldnames, "data": data})  # Return as JSON response
    except Exception as e:
        return jsonify({"error": str(e)}), 500

############################### WIKI ####################################
# Path to the directory containing your text files
TEXT_FILES_DIR = os.path.join(os.getcwd(), 'data', 'rules')


# Route to fetch a list of all available rule text files
@app.route('/api/rules', methods=['GET'])
def get_rules():
    try:
        # List all .txt files in the rules directory
        rule_files = [os.path.splitext(f)[0] for f in os.listdir(TEXT_FILES_DIR) if f.endswith('.txt')]
        return jsonify({"rules": rule_files})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    

@app.route('/api/rules/<string:rule_id>', methods=['GET'])
def get_rule(rule_id):
    """
    Fetch the content of a rule text file based on the rule ID.
    """
    try:
        # Construct the file path
        file_path = os.path.join(TEXT_FILES_DIR, f"{rule_id}.txt")
        
        # Check if file exists
        if not os.path.exists(file_path):
            return jsonify({"error": "File not found"}), 404
        
        # Read and return the file content
        with open(file_path, 'r') as file:
            content = file.read()
        return jsonify({"rule_id": rule_id, "content": content})
    except Exception as e:
        return jsonify({"error": str(e)}), 500



# Define the path to the backend folder containing the RuleCreation.py
BACKEND_FOLDER = os.path.join(os.getcwd(), 'data')
print(BACKEND_FOLDER)

# Route to serve RuleCreation.py for download
@app.route('/api/download/rule-python', methods=['GET'])
def download_rule_python():
    try:
        # Check if the file exists
        file_name = "RuleCreation.py"
        file_path = os.path.join(BACKEND_FOLDER, file_name)
        if not os.path.exists(file_path):
            return jsonify({"error": "File not found"}), 404
        
        # Serve the file
        return send_from_directory(BACKEND_FOLDER, file_name, as_attachment=True, mimetype='text/x-python')
    except Exception as e:
        return jsonify({"error": str(e)}), 500

############################### ERROR ####################################

# Path to the Log file for Error Page
ERROR_LOG_PATH = os.path.join(os.path.dirname(__file__),'data','logfiles','error.log')

def group_log_lines(file_path):
    """
    Groups log lines by detecting new log entries that start with a timestamp.
    Assumes that a new log entry begins with a line that starts with a 4-digit year.
    """
    grouped_logs = []
    current_block = ""
    # Regular expression to detect a new log entry based on a timestamp at the beginning of the line.
    timestamp_pattern = re.compile(r'^\d{4}-\d{2}-\d{2}')
    
    with open(file_path, 'r') as f:
        for line in f:
            line = line.rstrip()  # Remove any trailing newline characters.
            if timestamp_pattern.match(line):
                # If we already have a block, start a new one.
                if current_block:
                    grouped_logs.append(current_block)
                current_block = line  # Start a new block
            else:
                # Append subsequent lines to the current block.
                current_block += "\n" + line
        # Append the final block if it exists.
        if current_block:
            grouped_logs.append(current_block)
    return grouped_logs

@app.route('/api/errors', methods=['GET'])
def get_error_logs():
    if os.path.exists(ERROR_LOG_PATH):
        try:
            logs = group_log_lines(ERROR_LOG_PATH)
             # Retrieve only the latest 50 groups. If there are fewer, return all. 
            latest_logs = logs[-50:] if len(logs) >= 1 else logs

            return jsonify(latest_logs)
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    else:
        return jsonify({"message": "No error log found."}), 404


if __name__ == '__main__':
    app.run(debug=True)
