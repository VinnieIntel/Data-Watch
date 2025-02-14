import pandas as pd
import os

script_dir = os.path.dirname(__file__)
data_path = os.path.join(script_dir, 'data')
status_full_csv_path = os.path.join(data_path, "toolstatus_full.csv")
status_show_csv_path = os.path.join(data_path, "toolstatus_show.csv")
tools = [
    'HXV001', 'HXV002', 'HXV003', 'HXV004', 'HXV005', 'HXV006', 'HXV007', 'HXV008', 'HXV009', 'HXV010',
    'HXV011', 'HXV012', 'HXV013', 'HXV015', 'HXV016', 'HXV017', 'HXV201', 'HXV202', 'HXV203', 'HXV204',
    'HXV205', 'HXV206', 'HXV207', 'HXV208', 'HXV209', 'HXV210', 'HMV801', 'HMV802', 'HMV803', 'HMV804',
    'HMV805', 'HMV806', 'HMV807'
]

df_full = pd.read_csv(status_full_csv_path)
df_filtered = df_full[df_full['TOOL'].isin(tools)]
df_filtered = df_filtered.sort_values(by=['TOOL', 'TIMESTAMP'], ascending=[True, False])
df_latest = df_filtered.drop_duplicates(subset='TOOL', keep='first')

df_tools = pd.DataFrame(tools, columns=['TOOL'])
df_result = pd.merge(df_tools, df_latest[['TOOL', 'STATUS', 'TIMESTAMP']], on='TOOL', how='left')
df_result['STATUS'] = df_result['STATUS'].fillna('-')
df_result['TIMESTAMP'] = df_result['TIMESTAMP'].fillna('-')

# Save the result to a new CSV file
df_result.to_csv(status_show_csv_path, index=False)
