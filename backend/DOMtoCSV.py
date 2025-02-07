#REV2.1.1
#RuleProcessor class to encapsulate all rules (scalability)
#Failed rows append to trigger csv
#REV4.1
#append vinnie's process_log_files and append_to_csv

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
from collections import OrderedDict
import base64

current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# Define fixed headers
fixed_headers =['tool_id', 'lot_id']
# fixed_headers =['tool_id', 'cell_id']
# Define type1 prefix
# type1_prefixes = ['visualid', 'dvtsteddt', 'curfbin', 'prttesterid', 'thermalhdid', 'tiuid']
# Define type2 prefix
# type2_prefixes = ['tname_PCS_SOT']
type2_prefixes = 'tname_'

# Python logging
# log_file_path = r'C:\Users\soonthia\Python projects\DOM ituff processor\log.txt'
log_dir = r"C:\Projects\DataWatchUI\backend\data\logfiles"
os.makedirs(log_dir, exist_ok=True)

log_file_path = os.path.join(log_dir, "logfile_DOMtoCSV.log")

# Common log format
log_format = '%(asctime)s - %(levelname)s - %(message)s'

logging.basicConfig(
    level=logging.INFO,
    format=log_format,
    handlers=[
        logging.FileHandler(log_file_path),
        logging.StreamHandler(),  # Uncomment this line if you also want to print to the console
    ]
)

# --- Error Logger: logs only errors with full details ---
error_logger = logging.getLogger('error_logger')
error_logger.setLevel(logging.WARNING) # Capture both WARNING and ERROR levels

# Create file handler for error logs
error_handler = logging.FileHandler(os.path.join(log_dir, 'error.log'))
error_handler.setLevel(logging.WARNING)

# Set formatter to include timestamp, ERROR keyword, and message
formatter = logging.Formatter(log_format)
error_handler.setFormatter(formatter)

# Add handler to error_logger
error_logger.addHandler(error_handler)



# --- Example Usage ---
logging.info("This is an informational message.") #  in main log only
logging.error("This is a general error message.")  # in main log only
logging.warning("This is a warning message!") #  in main log only
error_logger.error("Critical system failure detected!")  # in both main and error.log
error_logger.warning("Disk space running low!") # in both main and error.log


# Another example of catching exceptions and logging them 
try:
    1 / 0  # Will cause ZeroDivisionError
except Exception as e:
    error_logger.error("An exception occurred: %s", e)


def get_base64_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

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
        rule_desc = "1. ALL SOT invalid reading\n2. B9726 AND one or more SOT invalid reading"
        specific_prefix = 'PCS_SOT'  # Define the specific prefix for SOT values
        
        # Path to the image file
        image1_path = "RFC/Data Watch - HDMx OOP RFC.png"
        image2_path = "RFC/Data Watch - TCUI VID Search.png"
        base64_image1 = get_base64_image(image1_path)
        base64_image2 = get_base64_image(image2_path)
        
        for data_set in all_data_sets:
            # variables
            tool_id = data_set.get('tool_id', 'Unknown')
            site_id = data_set.get('siteid', 'Unknown')
            visual_id = data_set.get('visualid', 'Unknown')
            lot_id = data_set.get('lot_id', 'Unknown')
            email_message = f"Hi MEOS, \n\nThere is potential OOP/FM unit {visual_id} triggered at {tool_id}_{site_id}, please refer to RFC below:\n"   
            
            # Convert float
            sot_values = []
            for key in data_set:
                if key.startswith(specific_prefix):
                    value = data_set[key]
                    if value is not None:
                        try:
                            sot_values.append(float(value))
                        except ValueError:
                            error_logger.warning(f"Non-numeric value encountered for key {key}: {value}")

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
                # Subject
                subject = f"Potential OOP / FM at {tool_id}_{site_id} - Lot: {lot_id} VID: {visual_id}"
                # Filter the dataset to include only the desired columns
                desired_columns = ['lot_id', 'visualid', 'tool_id', 'siteid', 'thermalhdid', 'prttesterid', 'tiuprscdid', 'curfbin', 'dvtststdt', 'dvtsteddt']
                # Include columns with prefix 'PCS_SOT'
                pcs_sot_columns = [key for key in data_set if key.startswith('PCS_SOT')]
                desired_columns.extend(pcs_sot_columns)
                # Filter the dataset to include only the desired columns
                filtered_data = {key: data_set.get(key, 'N/A') for key in desired_columns}
                # Body
                #body = "\n".join(f"{key}: {value}" for key, value in filtered_data.items()) + f"\nRule Name: {rule_name}\nRule Description: \n{rule_desc}"
                # Construct the email body with an HTML table
                #Hi MEOS, \n\nThere is potential OOP/FM unit {visual_id} triggered at {tool_id}_{site_id}, please \n1. Down TIU in CMMS\n2. Get ES to check on triggered cell\n3. Reroute lot {lot_id} to DVI\n\n
                body = f"""
                <html>
                <body>
                    <pre>{email_message}</pre>
                    <table border="1" style="border-collapse: collapse;">
                        <tr>
                """
                for key in filtered_data.keys():
                    body += f"<th>{key}</th>"
                body += "</tr><tr>"
                for value in filtered_data.values():
                    body += f"<td>{value}</td>"
                body += f"""
                        </tr>
                    </table>
                    <img src="data:image/png;base64,{base64_image1}" alt="Embedded Image" />
                    <img src="data:image/png;base64,{base64_image2}" alt="Embedded Image" />
                    <pre>\nRule Name: {rule_name}\nDescription: \n{rule_desc}</pre>
                    <pre>\nPLEASE COPY CSV FILE TO YOUR LOCAL SYSTEM BEFORE OPENING! \nRaw Data: {output_csv_path}\nTrigger Data: {trigger_csv_path}</pre>
                </body>
                </html>
                """ 
                send_email_outlook(
                    subject=subject,
                    body=body,
                    recipients=["soon.thiam.ong@intel.com"],
                    #recipients=["soon.thiam.ong@intel.com", "pgat.test.meos@intel.com"],
                    is_html=True
                )
            elif severity == 'medium' and data_set.get('curfbin') == '9726':
                logging.info(f"Row with severity {severity}: curfbin 9726 detected in medium severity row: {data_set}")
                # Subject
                subject = f"Potential OOP / FM at {tool_id}_{site_id} - Lot: {lot_id} VID: {visual_id}"
                # Filter the dataset to include only the desired columns
                desired_columns = ['lot_id', 'visualid', 'tool_id', 'siteid', 'thermalhdid', 'prttesterid', 'tiuprscdid', 'curfbin', 'dvtststdt', 'dvtsteddt']
                # Include columns with prefix 'PCS_SOT'
                pcs_sot_columns = [key for key in data_set if key.startswith('PCS_SOT')]
                desired_columns.extend(pcs_sot_columns)
                # Filter the dataset to include only the desired columns
                filtered_data = {key: data_set.get(key, 'N/A') for key in desired_columns}

                # body
                body = f"""
                <html>
                <body>
                    <pre>{email_message}</pre>
                    <table border="1" style="border-collapse: collapse;">
                        <tr>
                """
                for key in filtered_data.keys():
                    body += f"<th>{key}</th>"
                body += "</tr><tr>"
                for value in filtered_data.values():
                    body += f"<td>{value}</td>"
                body += f"""
                        </tr>
                    </table>
                    <pre>\nRule Name: {rule_name}\nDescription: \n{rule_desc}</pre>
                    <pre>\nPLEASE COPY CSV FILE TO YOUR LOCAL SYSTEM BEFORE OPENING! \nRaw Data: {output_csv_path}\nTrigger Data: {trigger_csv_path}</pre>
                </body>
                </html>
                """ 
                send_email_outlook(
                    subject=subject,
                    body=body,
                    recipients=["soon.thiam.ong@intel.com"],
                    #recipients=["soon.thiam.ong@intel.com", "pgat.test.meos@intel.com"],
                    #recipients=["soon.thiam.ong@intel.com", "pgat.test.meos@intel.com", "pgat.test.mtse@intel.com", "pgat.hdmx.es@intel.com"],
                    is_html=True
                )

    # Define more rules as methods here
    # def rule_x(self, all_data_sets, ...):
    #     ...
    # def rule_y(self, all_data_sets, ...):
    #     ...

    def get_failed_rows(self):
        return self.failed_rows

# Email function
def send_email_outlook(subject, body, recipients, cc_recipients=None, bcc_recipients=None, is_html=False):
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
        if is_html:
            mail.HTMLBody = body
        else:
            mail.Body = body
        mail.Send()
    finally:
        # Uninitialize COM for the current thread
        pythoncom.CoUninitialize()

# ituff processor function
def process_log_files(lines, tool_id):
    all_data_sets = []  # list to store all processed data sets
    dynamic_headers = set()  # keep track of dynamic headers encountered in the log files

    data_set = OrderedDict()  # an ordered dictionary to store the current data set
    capture_data = False  # Flag to indicate when to start capturing data
    first_skip = False

    for i, line in enumerate(lines):
        if "DBG DomItuffSubscriber: Processing Unit on Site:" in line:
            if not first_skip:
                # Extract the lot_id from the first occurrence
                lot_id_match = re.search(r"Lot:([A-Za-z0-9]+)", line)
                if lot_id_match:
                    lot_id = lot_id_match.group(1).strip()
                # Skip the first occurrence
                first_skip = True
                continue
            else:
                # Start capturing data from the second occurrence
                if data_set:  # If there is an existing data set, add it to the list of all data sets
                    all_data_sets.append(data_set)
                data_set = OrderedDict()  # Create a new data set
                data_set['tool_id'] = tool_id  # Set the tool_id value for the new data set
                if lot_id:
                    data_set['lot_id'] = lot_id  # Add lot_id to the data_set
                capture_data = True  
                # # Extract the cell_id from the line
                # cell_id_match = re.search(r"Processing Unit on Site: (.+)$", line)
                # if cell_id_match:
                #     cell_id = cell_id_match.group(1).strip()
                #     data_set['cell_id'] = cell_id  # Add cell_id to the data_set
                continue

        # Check for the end of the current data set
        if "_trslt_" in line :
            capture_data = False
            first_skip = False
            # Append the current data_set to all_data_sets before resetting
            if data_set:
                all_data_sets.append(data_set)
                data_set = OrderedDict()  # Reset the data_set for the next block of data
            continue

        comnt_mrslt_match = re.match(r"\d+_comnt_mrslt_([A-Za-z0-9_]+)_(.+)", line)
        comnt_match = re.search(r"\d+_comnt_((?:[A-Za-z0-9_]+::)?[A-Za-z0-9_]+(?:_[A-Za-z0-9_]+)*)_(\w+)$", line)

        # Capture data if the flag is set
        if capture_data:
        
            # Use regular expressions to capture variable names and values
            if type2_prefixes in line:
                #print(line)
                matches = re.findall(r"\d+_tname_([A-Za-z0-9_]+)", line)
                for token in matches:
                    dynamic_headers.add(token)
                    if token not in data_set:
                        data_set[token] = None  # Initialize with None
                    next_line = lines[i + 1].strip() if i + 1 < len(lines) else ""
                    if next_line.__contains__("_mrslt_"):
                        value = next_line.split("_mrslt_")[-1].strip()
                        data_set[token] = value
                    if next_line.__contains__("_strgval_"):
                        value = next_line.split("_strgval_")[-1].strip()
                        data_set[token] = value

            elif re.match(r"\d+_mrslt_\d+", line) or re.match(r"\d+_strgval_.+", line):
                continue

            else:
                if comnt_mrslt_match:
                    variable_name = comnt_mrslt_match.group(1)
                    variable_value = comnt_mrslt_match.group(2)
                    data_set[variable_name] = variable_value
                    dynamic_headers.add(variable_name)
                elif comnt_match:
                    variable_name = comnt_match.group(1)
                    variable_value = comnt_match.group(2)
                    data_set[variable_name] = variable_value
                    dynamic_headers.add(variable_name)
                    

                else:
                    variable_match = re.search(r"(\d+)_(\w+)_([^_]*)", line)
                    #print(variable_match)
                    if variable_match:
                        # Extract the variable name and value
                        variable_name = variable_match.group(2)

                        variable_value = variable_match.group(3).strip()
                        # Add the variable to the data set
                        data_set[variable_name] = variable_value
                        # Add the variable name to the set of dynamic headers
                        dynamic_headers.add(variable_name)

    # Check if there is a remaining data_set to add to all_data_sets
    if data_set:
        all_data_sets.append(data_set)

    return all_data_sets, dynamic_headers


###################### Append to CSV functions ###################################
def append_to_csv(csv_file_path, all_data_sets, dynamic_headers):
    with csv_file_lock:
        # Check if the CSV file already exists to determine if we need to write headers
        file_exists = os.path.isfile(csv_file_path)
        
        # Combine fixed headers, type1 prefixes, and sorted dynamic headers
        sorted_dynamic_headers = sorted(dynamic_headers)
        csv_headers = fixed_headers  + sorted_dynamic_headers

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
                error_logger.warning(f"Permission denied: {e}. Retrying...")
                
                time.sleep(5)  # Wait for 5 seconds before retrying
                attempts -= 1
            except Exception as e:
                error_logger.error(f"An error occurred: {e}. Retrying...")
                error_logger.error(traceback.format_exc())

                time.sleep(5)  # Wait for 5 seconds before retrying
                attempts -= 1
        if attempts == 0:
            error_logger.error(f"Failed to process file {file_path} after multiple attempts.")
            
        
        
# Base directory where the HXV folders are located
base_log_files_dir = r'\\t3file1.png.intel.com\offline_logs\hdmx\ST'

# List of folder names to monitor
folders_to_monitor = ['test1', 'test2']
#folders_to_monitor = ['HXV001','HXV002','HXV003','HXV004','HXV005','HXV006','HXV007','HXV008','HXV009','HXV010','HXV011','HXV012','HXV013','HXV015','HXV016','HXV017','HXV201','HXV202','HXV203','HXV204','HXV205','HXV206','HXV207','HXV208','HXV209','HXV210','HMV801','HMV802','HMV803','HMV804','HMV805','HMV806','HMV807']

# Define the output CSV file path (single file for all folders)
output_csv_path = r'C:\Projects\datawatchUI\backend\data\Raw_Data_TEST.csv'
trigger_csv_path = r'C:\Projects\datawatchUI\backend\data\Trigger_Data_TEST.csv'

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
