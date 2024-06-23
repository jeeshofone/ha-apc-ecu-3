import requests
from bs4 import BeautifulSoup

def generate_yaml(url_or_path):
    if url_or_path.startswith('http://') or url_or_path.startswith('https://'):
        # URL
        r = requests.get(url_or_path)
        if r.status_code != 200:
            print('Error: ', r.status_code)
            return
        html_content = r.text
    else:
        # Local file path
        with open(url_or_path, 'r') as file:
            html_content = file.read()
    
    soup = BeautifulSoup(html_content, 'html.parser')
    table = soup.find('table')

    if table is None:
        print('No table found')
        return

    rows = table.find_all('tr')
    inverter_ids = []

    for row in rows:
        columns = row.find_all('td')
        if len(columns) > 0:
            inverter_ids.append(columns[0].text.strip())

    print(f'Found {len(inverter_ids)} inverters')

    unique_ids = set(inverter_ids)  # Remove duplicate entries
 
    with open('config_part.yaml', 'w') as f:
        f.write('rest:\n')
        f.write('  - resource: http://homeassistant.local:8123/local/power_data.json\n')
        f.write('    sensor:\n')
        
        for id in unique_ids:
            panel_name = id.split('-')[0]  # Extract the panel name from the inverter ID
            for suffix in ['A', 'B']:
                if f"{panel_name}-{suffix}" in inverter_ids:
                    f.write(
                        f'      - name: "Solar Panel {panel_name} {suffix} power"\n'
                        f'        value_template: \'{{{{ value_json["{panel_name}-{suffix}"][0] }}}}\n'
                        f'        unit_of_measurement: "W"\n'
                        f'\n'
                        f'      - name: "Solar Panel {panel_name} {suffix} grid frequency"\n'
                        f'        value_template: \'{{{{ value_json["{panel_name}-{suffix}"][1] }}}}\n'
                        f'        unit_of_measurement: "Hz"\n'
                        f'\n'
                        f'      - name: "Solar Panel {panel_name} {suffix} grid voltage"\n'
                        f'        value_template: \'{{{{ value_json["{panel_name}-{suffix}"][2] }}}}\n'
                        f'        unit_of_measurement: "V"\n'
                        f'\n'
                        f'      - name: "Solar Panel {panel_name} {suffix} temperature"\n'
                        f'        value_template: \'{{{{ value_json["{panel_name}-{suffix}"][3] }}}}\n'
                        f'        unit_of_measurement: "°C"\n'
                        f'\n'
                    )

# Example usage with a web URL
# url = 'http://IP-OF-ECU-3/cgi-bin/parameters'
# url = 'http://IP-OF-ECU-4/index.php/realtimedata'
# generate_yaml(url)

# Example usage with a local file path
file_path_v4 = 'html-examples/ECU-v3.10.5.html'
generate_yaml(file_path_v4)
