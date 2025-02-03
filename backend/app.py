from flask import Flask, jsonify, send_from_directory
from flask_cors import CORS
import os
import csv

app = Flask(__name__)
CORS(app)  # Enable CORS to allow React to access the API

############################### HOME ####################################
# Path to the CSV file
DATA_PATH = os.path.join(os.path.dirname(__file__), 'data', 'output_2.csv')

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
STATUS_PATH = os.path.join(os.path.dirname(__file__), 'data', 'status.csv')

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

if __name__ == '__main__':
    app.run(debug=True)
