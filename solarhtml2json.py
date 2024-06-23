import requests
from bs4 import BeautifulSoup
from datetime import datetime
import json
import os

def get_power_data(file_path=None, is_ecu_v4=False):
    if file_path and os.path.exists(file_path):
        with open(file_path, 'r') as f:
            html_content = f.read()
    else:
        url = 'http://IP-OF-ECU-3/cgi-bin/parameters'
        r = requests.get(url)
        if r.status_code != 200:
            print('Error: ', r.status_code)
            return
        
        html_content = r.text

    soup = BeautifulSoup(html_content, 'html.parser')
    table = soup.find('table')
    
    if table is None:
        print('No table found')
        return

    rows = table.find_all('tr')
    power_data = {}

    # Function to clean and convert value
    def clean_value(value, replace_dict):
        for key, replacement in replace_dict.items():
            value = value.replace(key, replacement)
        return '0' if value.strip() in ['', '-', '\xa0'] else value.strip()

    if is_ecu_v4:
        for i in range(1, len(rows) - 1, 2):  # Process two rows at a time, ensure even indexing.
            row_a = rows[i]
            row_b = rows[i + 1] if i + 1 < len(rows) else None
            columns_a = row_a.find_all('td')
            columns_b = row_b.find_all('td') if row_b else []

            # Debug: Print rows being processed
            print(f"Processing rows {i}, {i + 1}")
            print(f"Row A columns: {len(columns_a)}, Row B columns: {len(columns_b) if columns_b else 'None'}")
            
            if len(columns_a) == 6 and len(columns_b) == 3:
                base_id_a = columns_a[0].text.strip()
                base_id_b = columns_b[0].text.strip()

                common_grid_freq = clean_value(columns_a[2].text, {'Hz': ''})
                common_temp = clean_value(columns_a[4].text, {'°C': ''})
                common_report_time = columns_a[5].text.strip() if columns_a[5].text.strip() else datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                
                power_data[base_id_a] = [clean_value(columns_a[1].text, {'W': ''}),  # power (A)
                                         clean_value(columns_a[3].text, {'V': ''}),  # voltage (A)
                                         common_grid_freq,  # grid frequency (shared)
                                         common_temp,  # temperature (shared)
                                         common_report_time]  # reporting time (shared)
                
                power_data[base_id_b] = [clean_value(columns_b[1].text, {'W': ''}),  # power (B)
                                         clean_value(columns_b[2].text, {'V': ''}),  # voltage (B)
                                         common_grid_freq,  # grid frequency (shared)
                                         common_temp,  # temperature (shared)
                                         common_report_time]  # reporting time (shared)

                # Debug: Print debug information
                print(f"Extracted values for {base_id_a}: {power_data[base_id_a]}")
                print(f"Extracted values for {base_id_b}: {power_data[base_id_b]}")
    else:
        for row in rows[1:]:  # Skip the header row
            columns = row.find_all('td')
            if len(columns) == 6:
                base_id = columns[0].text.strip()
                power_data[base_id] = [clean_value(columns[1].text, {'W': ''}),
                                       clean_value(columns[2].text, {'Hz': ''}),
                                       clean_value(columns[3].text, {'V': ''}),
                                       clean_value(columns[4].text, {'°C': ''}),
                                       columns[5].text.strip()]

    # For missing panels (offline overnight, etc.) fill in the latest timestamp found.
    latest_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    for panel in power_data:
        if len(power_data[panel]) >= 5 and (not power_data[panel][4] or power_data[panel][4] == '-'):
            power_data[panel][4] = latest_time

    with open('www/power_data.json', 'w') as outfile:
        json.dump(power_data, outfile, indent=4)

    print("Final power data:", json.dumps(power_data, indent=4))

# Example usage
#get_power_data(file_path='html-examples/ECU-v3.10.5.html', is_ecu_v4=False)
get_power_data(file_path='html-examples/ECU-v4.html', is_ecu_v4=True)
