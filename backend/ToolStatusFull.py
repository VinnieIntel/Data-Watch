import cx_Oracle
import pandas as pd
import os
import sys
import subprocess

script_dir = os.path.dirname(__file__)
data_path = os.path.join(script_dir, 'data')
next_script_path = os.path.join(script_dir, 'ToolStatusShow.py')
status_full_csv_path = os.path.join(data_path, "toolstatus_full.csv")

# Establish the connection
con_mars = cx_Oracle.connect("", "", "PG.[A12_PROD_0.].MARS")

# Define the SQL query
sql_mars = """
SELECT 
          facility AS facility
         ,entity AS entity
         ,To_Char(txn_timestamp,'yyyy-mm-dd hh24:mi:ss') AS Timestamp
         ,parent_entity AS Tool
         ,tool_instance_name AS tool_instance_name
         ,ept_state AS Status
         ,task_name AS task_name
         ,elapse_seconds AS elapse_seconds
         ,manual_state_code AS manual_state_code
         ,comments AS comments
         ,upper_state AS upper_state
         ,WW AS WW
         ,next_task_name AS next_task_name
         ,LEAD ( elapse_seconds ,1,NULL) OVER (PARTITION BY entity ORDER BY txn_timestamp, tool_instance_name ASC) AS next_task_duration
FROM
(
SELECT  
          facility AS facility
         ,entity AS entity
         ,txn_timestamp AS txn_timestamp
         ,txn_load_date AS txn_load_date
         ,parent_entity AS parent_entity
         ,entity_type AS entity_type
         ,tool_instance_name AS tool_instance_name
         ,ept_state_type AS ept_state_type
         ,ept_state AS ept_state
         ,blocked_reason_text AS blocked_reason_text
         ,task_name AS task_name
         ,elapse_seconds AS elapse_seconds
         ,manual_state_code AS manual_state_code
         ,comments AS comments
         ,next_txn_timestamp AS next_txn_timestamp
         ,blocked_reason_code AS blocked_reason_code
         ,automated_state_code AS automated_state_code
         ,ept_type AS ept_type
         ,upper_state AS upper_state
         ,WW AS WW
         ,task AS task
         ,previous_state_code AS previous_state_code
         ,previous_task_code AS previous_task_code
         ,previous_task_name AS previous_task_name
         ,next_task_name AS next_task_name
FROM 
(
SELECT aept6.*
         ,aept6.eptstate9999 AS ept_state
         ,UPPER( aept6.eptstate9999 ) AS upper_state
FROM
(
SELECT '1' AS a
         ,aept1.entity AS entity
         ,aept1.parent_entity AS parent_entity
         ,aept1.entity_type AS entity_type
         ,aept1.tool_instance_name AS tool_instance_name
         ,aept1.ept_state_type AS ept_state_type
         ,LEAD ( aept5.task_name ,1,NULL) OVER (PARTITION BY aept1.entity ORDER BY aept2.txn_timestamp, aept1.tool_instance_name ASC) AS next_task_name
         ,aept5.blocked_reason_text AS blocked_reason_text
         ,aept5.task_name AS task_name
         ,CASE WHEN ( aept5.task_name = 'EndLotStarted'  ) THEN 'EndLot' 
WHEN ( aept5.task_name = 'EndLotCompleted'  ) THEN 'EndLot' 
ELSE  aept5.task_name END
AS task
         ,aept5.previous_state_code AS previous_state_code
         ,aept5.previous_task_code AS previous_task_code
         ,aept5.previous_task_name AS previous_task_name
         ,aept2.facility AS facility
         ,aept2.txn_timestamp AS txn_timestamp
         ,aept2.load_date AS txn_load_date
         ,aept2.elapse_seconds AS elapse_seconds
         ,aept2.manual_state_code AS manual_state_code
         ,aept2.next_txn_timestamp AS next_txn_timestamp
         ,aept2.blocked_reason_code AS blocked_reason_code
         ,aept2.automated_state_code AS automated_state_code
         ,aept2.ept_type AS ept_type
         ,TO_CHAR( (aept2.txn_timestamp) + 7 - TO_CHAR( (aept2.txn_timestamp) ,'d') ,'yyyyww') AS WW
         ,aept3.comments AS comments
,CASE
WHEN aept2.ept_type = 'E116' THEN
CASE
WHEN aept2.automated_state_code = 0 THEN 'STANDBY'
WHEN aept2.automated_state_code = 3 THEN 'Unknown'
WHEN aept2.automated_state_code = 1 AND aept2.task_code In (0,1,2,3) THEN 'PROD'
WHEN aept2.automated_state_code = 1 AND aept2.task_code In (4,5) THEN 'SCDL DT'
WHEN aept2.automated_state_code = 1 AND aept2.task_code = 6 THEN 'Between Unit-Carrier'
WHEN aept2.automated_state_code = 2 AND aept2.blocked_reason_code In (1,2,3,4,5,7,8,9,0) THEN 'UNSCDL DT'
WHEN aept2.automated_state_code = 2 AND aept2.blocked_reason_code = 6 THEN 'STANDBY'
WHEN aept2.automated_state_code in (1,2) THEN aept5.Task_Name
END
WHEN aept2.ept_type = 'MANUAL' THEN
CASE
WHEN aept2.Manual_State_Code = 'AUTO ENG' Then 'ENG TIME'
WHEN aept2.Manual_State_Code = 'ENG' Then 'ENG TIME'
WHEN aept2.Manual_State_Code = 'EQP ENG' Then 'ENG TIME'
WHEN aept2.Manual_State_Code = 'NON SCDL TIME' Then 'NON SCDL TIME'
WHEN aept2.Manual_State_Code = 'NPI ENG' Then 'ENG TIME'
WHEN aept2.Manual_State_Code = 'PM CLOSED' Then 'PM'
WHEN aept2.Manual_State_Code = 'PM OVERDUE' Then 'PM'
WHEN aept2.Manual_State_Code = 'PROD ENG' Then 'ENG TIME'
WHEN aept2.Manual_State_Code = 'PROD TEST' Then 'ENG TIME'
WHEN aept2.Manual_State_Code = 'WAIT FSE S' Then 'WAIT FSE'
WHEN aept2.Manual_State_Code = 'WAIT FSE U' Then 'WAIT FSE'
WHEN aept2.Manual_State_Code = 'WAIT TECH S' Then 'WAIT TECH'
WHEN aept2.Manual_State_Code = 'WAIT TECH U' Then 'WAIT TECH'
ELSE   aept2.Manual_State_Code
END
ELSE aept2.Manual_State_Code END AS eptstate9999
FROM
A12_PROD_0.F_EPT_Entity aept1
,A12_PROD_0.F_EPT_Entity_StateHist aept2
,A12_PROD_0.F_EPT_StateHist_Detail aept5
,A12_PROD_0.F_EPT_Comment aept3
WHERE 1=1
AND      aept1.entity = aept2.entity
AND      aept2.statehist_id = aept5.statehist_id (+)
AND      aept2.entity = aept3.entity (+)
AND      aept2.txn_timestamp = aept3.comment_timestamp (+)
AND      (aept1.entity LIKE  'HXV%'
) 
AND      aept2.load_date >= TRUNC(SYSDATE) - 1 
AND      (aept1.tool_instance_name LIKE  'ToolController%'
) 
) aept6 WHERE 1=1
) WHERE 1=1
)
"""

# Execute the query and store the result in a DataFrame
df_mars = pd.read_sql(sql_mars, con_mars)

# Save the DataFrame to a CSV file
df_mars.to_csv(status_full_csv_path, index=False)

# Close the connection
con_mars.close()

# Call next process
python_executable = sys.executable
subprocess.run([python_executable, next_script_path])