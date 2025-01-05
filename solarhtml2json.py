import requests
from bs4 import BeautifulSoup
from datetime import datetime
import json
import os
import argparse
import re

def clean_value(value, replace_dict, is_temperature=False):
    for key, replacement in replace_dict.items():
        value = value.replace(key, replacement)
    cleaned_value = value.strip()
    if is_temperature:
        cleaned_value = re.sub(r'[^\d.]+', '', cleaned_value)  # Remove everything except digits and dot
    return '0' if cleaned_value in ['', '-', '�'] else cleaned_value

def get_html_content(file_path, url):
    if file_path and os.path.exists(file_path):
        with open(file_path, 'r') as f:
            html_content = f.read()
    else:
        r = requests.get(url)
        if r.status_code != 200:
            print('Error:', r.status_code)
            return None
        html_content = r.text
    return html_content

def parse_table(html_content, is_ecu_v4):
    soup = BeautifulSoup(html_content, 'html.parser')
    table = soup.find('table')
    
    if table is None:
        print('No table found')
        return None

    rows = table.find_all('tr')
    power_data = {}

    latest_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    if is_ecu_v4:
        for i in range(1, len(rows) - 1, 2):
            row_a = rows[i]
            row_b = rows[i + 1] if i + 1 < len(rows) else None
            columns_a = row_a.find_all('td')
            columns_b = row_b.find_all('td') if row_b else []

            if len(columns_a) == 6 and len(columns_b) == 3:
                base_id_a = columns_a[0].text.strip()
                base_id_b = columns_b[0].text.strip()

                common_grid_freq = clean_value(columns_a[2].text, {'Hz': ''})
                common_temp = clean_value(columns_a[4].text, {'°C': ''}, is_temperature=True)
                common_report_time = columns_a[5].text.strip() if columns_a[5].text.strip() else latest_time
                
                power_data[base_id_a] = [clean_value(columns_a[1].text, {'W': ''}),
                                         clean_value(columns_a[3].text, {'V': ''}),
                                         common_grid_freq,
                                         common_temp,
                                         common_report_time]
                
                power_data[base_id_b] = [clean_value(columns_b[1].text, {'W': ''}),
                                         clean_value(columns_b[2].text, {'V': ''}),
                                         common_grid_freq,
                                         common_temp,
                                         common_report_time]
    else:
        for row in rows[1:]:
            columns = row.find_all('td')
            if len(columns) == 6:
                base_id = columns[0].text.strip()
                power_data[base_id] = [clean_value(columns[1].text, {'W': ''}),
                                       clean_value(columns[2].text, {'Hz': ''}),
                                       clean_value(columns[3].text, {'V': ''}),
                                       clean_value(columns[4].text, {'°C': ''}, is_temperature=True),
                                       columns[5].text.strip() if columns[5].text.strip() else latest_time]

    return power_data

def save_power_data(power_data):
    with open('www/power_data.json', 'w') as outfile:
        json.dump(power_data, outfile, indent=4)

def generate_yaml_from_json():
    with open('www/power_data.json', 'r') as f:
        power_data = json.load(f)

    inverter_ids = power_data.keys()

    config = 'rest:\n'
    config += '  - resource: http://homeassistant.local:8123/local/power_data.json\n'
    config += '    sensor:\n'
    
    panel_names = set()
    
    for id in inverter_ids:
        panel_name = id.split('-')[0]
        suffix = id.split('-')[1]
        panel_names.add(f'solar_panel_{panel_name.lower()}_{suffix.lower()}')
        unique_id_base = f"solar_panel_{panel_name.lower()}_{suffix.lower()}_"
        config += (
            f'      - name: "Solar Panel {panel_name} {suffix} power"\n'
            f'        unique_id: "{unique_id_base}power"\n'
            f'        value_template: \'{{{{ value_json["{id}"][0] }}}}\'\n'
            f'        unit_of_measurement: "W"\n'
            f'      - name: "Solar Panel {panel_name} {suffix} grid voltage"\n'
            f'        unique_id: "{unique_id_base}grid_voltage"\n'
            f'        value_template: \'{{{{ value_json["{id}"][1] }}}}\'\n'
            f'        unit_of_measurement: "V"\n'
            f'      - name: "Solar Panel {panel_name} {suffix} grid frequency"\n'
            f'        unique_id: "{unique_id_base}grid_frequency"\n'
            f'        value_template: \'{{{{ value_json["{id}"][2] }}}}\'\n'
            f'        unit_of_measurement: "Hz"\n'
            f'      - name: "Solar Panel {panel_name} {suffix} temperature"\n'
            f'        unique_id: "{unique_id_base}temperature"\n'
            f'        value_template: \'{{{{ value_json["{id}"][3] }}}}\'\n'
            f'        unit_of_measurement: "°C"\n'
        )
    
    config += '\nsensor:\n'
    config += '  - platform: template\n'
    config += '    sensors:\n'
    config += '      solar_panels_total_power:\n'
    config += '        unique_id: "total_solar_power"\n'
    config += '        friendly_name: "Total Solar Power"\n'
    config += '        unit_of_measurement: "W"\n'
    
    panels_sum = ' +\n             '.join([f"states('sensor.{name}_power')|float(default=0)" for name in panel_names])
    config += (
        '        value_template: >\n'
        '          {{ (\n'
        f'             {panels_sum}\n'
        '          ) }}\n'
    )
    
    with open('config_part.yaml', 'w') as f:
        f.write(config)

def main():
    parser = argparse.ArgumentParser(description='Process and collect solar data.')
    parser.add_argument('--file', type=str, help='Path to local HTML file')
    parser.add_argument('--url', type=str, help='URL to fetch the HTML content')
    parser.add_argument('--ecu_v4', action='store_true', help='Enable ECU v4 parsing mode')
    parser.add_argument('--generate_config', action='store_true', help='Generate config_part.yaml from power_data.json')
    
    args = parser.parse_args()
    
    if args.generate_config:
        generate_yaml_from_json()
    else:
        html_content = get_html_content(args.file, args.url)
        if html_content:
            power_data = parse_table(html_content, args.ecu_v4)
            if power_data:
                save_power_data(power_data)

if __name__ == "__main__":
    main()
