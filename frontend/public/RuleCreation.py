#REV2.1.1
#RuleProcessor class to encapsulate all rules (scalability)
#Failed rows append to trigger csv


from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import time
import os
import csv
import re
import win32com.client as win32
import pythoncom
from datetime import datetime
from threading import Lock
import traceback
import logging
import re
from collections import OrderedDict

current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# Define fixed headers
fixed_headers =['tool_id', 'cell_id']
# Define type1 prefix
type1_prefixes = ['visualid', 'dvtsteddt', 'curfbin', 'prttesterid', 'thermalhdid', 'tiuid']
# Define type2 prefix
type2_prefixes = ['tname_PCS_SOT']

# Python logging
log_file_path = r'C:\Users\vtiang\Documents\VisualStudioProjects\ThirdEye\log.txt'
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_file_path),
        logging.StreamHandler()  # Uncomment this line if you also want to print to the console
    ]
)

########################################################################
########################## START OF RULE LIST ##########################
########################################################################

class RuleProcessor:
    def __init__(self):
        self.failed_rows = []

    def process_all_rules(self, all_data_sets, type2_prefixes):
        # Call each rule method here
        self.rule_oop_rev1(all_data_sets, type2_prefixes)
        # Add more rules as needed
        # self.rule_x(all_data_sets, ...)
        # self.rule_y(all_data_sets, ...)
        # ...

    def rule_oop_rev1(self, all_data_sets, type2_prefixes):
        rule_name = "rule_oop_rev1"
        for data_set in all_data_sets:
            # Convert float
            sot_values = [float(data_set[key]) for key in data_set if any(key.startswith(prefix) for prefix in type2_prefixes)]
            
            # Determine severity
            if not sot_values:
                severity = 'none'
            else:
                high_count = sum(value >= 255 for value in sot_values)
                if high_count == len(sot_values):
                    severity = 'high'
                elif 1 <= high_count < len(sot_values):
                    severity = 'medium'
                else:
                    severity = 'low'

            # Append failed data set
            if severity == 'high' or (severity == 'medium' and data_set.get('curfbin') == '9726'):
                failed_data_set = OrderedDict([("Rule", rule_name)] + list(data_set.items()))  # Add the rule name at the beginning
                self.failed_rows.append(failed_data_set)
            
            # Response based on severity
            if severity == 'high':
                logging.info(f"Row with severity {severity}: all SOT 255: {data_set}")
                tool_id = data_set.get('tool_id', 'Unknown')
                subject = f"{tool_id} Potential OOP / FM (TESTING PLS IGNORE)"
                body = "\n".join(f"{key}: {value}" for key, value in data_set.items())
                send_email_outlook(
                    subject=subject,
                    body=f"Triggered VID:\n{body}",
                    recipients=["soon.thiam.ong@intel.com"],
                )
            elif severity == 'medium' and data_set.get('curfbin') == '9726':
                logging.info(f"Row with severity {severity}: curfbin 9726 detected in medium severity row: {data_set}")
                tool_id = data_set.get('tool_id', 'Unknown')
                subject = f"{tool_id} Potential OOP / FM"
                body = "\n".join(f"{key}: {value}" for key, value in data_set.items())
                send_email_outlook(
                    subject=subject,
                    body=f"Triggered VID:\n{body}",
                    recipients=["soon.thiam.ong@intel.com"],
                )
    # Define more rules as methods here
    # def rule_x(self, all_data_sets, ...):
    #     ...
    # def rule_y(self, all_data_sets, ...):
    #     ...

    def get_failed_rows(self):
        return self.failed_rows


#-------------------------#
# RULE #1 - rule_oop_rev1 #
#-------------------------#
# def rule_oop_rev1(all_data_sets, type2_prefixes):
#     for data_set in all_data_sets:
#         # Convert float
#         sot_values = [float(data_set[key]) for key in data_set if any(key.startswith(prefix) for prefix in type2_prefixes)]
        
#         # Determine severity
#         if not sot_values:
#             severity = 'none'
#         else:
#             high_count = sum(value >= 255 for value in sot_values)
#             if high_count == len(sot_values):
#                 severity = 'high'
#             elif 1 <= high_count < len(sot_values):
#                 severity = 'medium'
#             else:
#                 severity = 'low'

#         # Response based on severity
#         if severity == 'high':
#             logging.info(f"Row with severity {severity}: all SOT 255: {data_set}")
#             tool_id = data_set.get('tool_id', 'Unknown')
#             subject = f"{tool_id} Potential OOP / FM"
#             body = "\n".join(f"{key}: {value}" for key, value in data_set.items())
#             send_email_outlook(
#                 subject=subject,
#                 body=f"Triggered VID:\n{body}",
#                 recipients=["soon.thiam.ong@intel.com"],
#             )
#         elif severity == 'medium' and data_set.get('curfbin') == '9726':
#             logging.info(f"Row with severity {severity}: curfbin 9726 detected in medium severity row: {data_set}")
#             tool_id = data_set.get('tool_id', 'Unknown')
#             subject = f"{tool_id} Potential OOP / FM"
#             body = "\n".join(f"{key}: {value}" for key, value in data_set.items())
#             send_email_outlook(
#                 subject=subject,
#                 body=f"Triggered VID:\n{body}",
#                 recipients=["soon.thiam.ong@intel.com"],
#             ) 
#-------------------------#
#-------------------------#

######################################################################
########################## END OF RULE LIST ##########################
######################################################################

# Email function
def send_email_outlook(subject, body, recipients, cc_recipients=None, bcc_recipients=None):
    # Initialize COM for current thread
    pythoncom.CoInitialize()

    try:
        outlook = win32.Dispatch('outlook.application')
        mail = outlook.CreateItem(0) 
        #diff email into single string separate by ;
        mail.To = "; ".join(recipients) 
        if cc_recipients:
            mail.CC = "; ".join(cc_recipients)
        if bcc_recipients:
            mail.BCC = "; ".join(bcc_recipients)  
        mail.Subject = subject
        mail.Body = body
        mail.Send()
    finally:
        # Uninitialize COM for the current thread
        pythoncom.CoUninitialize()

# ituff processor function
def process_log_files(lines, tool_id):
    all_data_sets = []
    dynamic_headers = set()

    data_set = OrderedDict()
    capture_data = False
    for i, line in enumerate(lines):
        if "DBG DomItuffSubscriber: Processing Unit on Site:" in line:
            if data_set:
                all_data_sets.append(data_set)
            data_set = OrderedDict((header, None) for header in fixed_headers + type1_prefixes)
            data_set['tool_id'] = tool_id 
            capture_data = True
            # Extract the cell_id
            parts = line.split(":")
            if len(parts) > 1:
                cell_id = parts[-1].strip()
                data_set['cell_id'] = cell_id 
            continue
        if "_trslt_" in line:
            capture_data = False
            continue
        if capture_data:
            for header in type1_prefixes:
                if f"_{header}_" in line:
                    value = line.split(f"_{header}_")[-1].strip()
                    data_set[header] = value
            
            for prefix in type2_prefixes:
                matches = re.findall(rf"{prefix}[A-Za-z0-9_]+", line)
                for token in matches:
                    dynamic_headers.add(token)
                    if token not in data_set:
                        data_set[token] = None  
                    next_line = lines[i + 1].strip() if i + 1 < len(lines) else ""
                    if next_line.startswith("2_mrslt_"):
                        value = next_line.split("2_mrslt_")[-1].strip()
                        data_set[token] = value

    # Add tool_id to each data set
    for data_set in all_data_sets:
        data_set['tool_id'] = tool_id
        
    return all_data_sets, dynamic_headers

###################### Append to CSV functions ###################################
def append_to_csv(csv_file_path, all_data_sets, dynamic_headers):
    with csv_file_lock:
        # Check if the CSV file already exists to determine if we need to write headers
        file_exists = os.path.isfile(csv_file_path)
        
        # Combine fixed headers, type1 prefixes, and sorted dynamic headers
        sorted_dynamic_headers = sorted(dynamic_headers)
        csv_headers = fixed_headers + type1_prefixes + sorted_dynamic_headers

        # Append to CSV
        with open(csv_file_path, 'a', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=csv_headers)
            if not file_exists:
                # Write the headers to the CSV file
                writer.writeheader()
            for data_set in all_data_sets:
                # Ensure each data_set dictionary has all the keys, default to None if not present
                for header in csv_headers:
                    data_set.setdefault(header, None)
                writer.writerow(data_set)

def append_failed_rows_to_csv(csv_file_path, failed_rows):
    with csv_file_lock:
        file_exists = os.path.isfile(csv_file_path)
        # The "Rule" column is already included as the first key in each failed row
        headers = list(failed_rows[0].keys()) if failed_rows else []

        with open(csv_file_path, 'a', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=headers)
            if not file_exists:
                writer.writeheader()
            for row in failed_rows:
                writer.writerow(row)
#######################################################################################


class LogFileHandler(FileSystemEventHandler):
    def __init__(self, log_files_dir, output_csv_path, tool_id):
        self.log_files_dir = log_files_dir
        self.output_csv_path = output_csv_path
        self.trigger_csv_path = trigger_csv_path
        self.tool_id = tool_id  # Add folder name as an attribute
        self.current_file = None
        self.file_position = 0

    def on_modified(self, event):
        logging.info(f"File modified: {event.src_path}")  # Debug print
        if not event.is_directory and "DomItuffSubscriber_" in event.src_path:
            self.process_new_lines(event.src_path)

    def on_created(self, event):
        logging.info(f"File created: {event.src_path}")  # Debug print
        if not event.is_directory and "DomItuffSubscriber_" in event.src_path:
            self.current_file = event.src_path
            self.file_position = 0  # Reset file position since this is a new file

    def process_new_lines(self, file_path):
        logging.info(f"Processing new lines in file: {file_path}")  # Debug print with timestamp
        
        attempts = 3
        while attempts > 0:
            try:
                with open(file_path, 'r') as file:
                    file.seek(self.file_position)
                    new_lines = file.readlines()
                    self.file_position = file.tell()
                
                # Process the new lines and append to CSV if there are any new lines
                if new_lines:
                    all_data_sets, dynamic_headers = process_log_files(new_lines, self.tool_id)
                    append_to_csv(self.output_csv_path, all_data_sets, dynamic_headers)
                    #rule_oop_rev1(all_data_sets, type2_prefixes)
                    
                    # Create an instance of RuleProcessor and process all rules
                    rule_processor = RuleProcessor()
                    rule_processor.process_all_rules(all_data_sets, type2_prefixes)

                    # Get the failed rows from all rules
                    failed_rows = rule_processor.get_failed_rows()
                    if failed_rows:
                        append_failed_rows_to_csv(self.trigger_csv_path, failed_rows)
                    
                    
                    
                break  # Exit the loop if successful
            except PermissionError as e:
                logging.warning(f"Permission denied: {e}. Retrying...")
                time.sleep(5)  # Wait for 5 seconds before retrying
                attempts -= 1
            except Exception as e:
                logging.error(f"An error occurred: {e}. Retrying...")
                logging.error(traceback.format_exc())
                time.sleep(5)  # Wait for 5 seconds before retrying
                attempts -= 1
        if attempts == 0:
            logging.error(f"Failed to process file {file_path} after multiple attempts.")
        
        
# Base directory where the HXV folders are located
base_log_files_dir = r'C:\Users\vtiang\Documents\VisualStudioProjects\ThirdEye'

# List of folder names to monitor
folders_to_monitor = ['test2']  # Add more folder names as needed

# Define the output CSV file path (single file for all folders)
output_csv_path = r'C:\Users\vtiang\Documents\VisualStudioProjects\ThirdEye\Output\output_1.csv'
trigger_csv_path = r'C:\Users\vtiang\Documents\VisualStudioProjects\ThirdEye\Output\trigger_1.csv'

# Create a lock object
csv_file_lock = Lock()

# Create an Observer
observer = Observer()

# Loop over the folder names and set up monitoring for each
for tool_id in folders_to_monitor:
    # Define the path to the specific log files directory
    log_files_dir = os.path.join(base_log_files_dir, tool_id)

    # Create an event handler for the specific folder
    event_handler = LogFileHandler(log_files_dir, output_csv_path, tool_id)

    # Schedule the event handler with the observer
    observer.schedule(event_handler, log_files_dir, recursive=False)

# Start the observer
observer.start()

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    observer.stop()
observer.join()
