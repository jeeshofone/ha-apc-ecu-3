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

    with open('config_part.yaml', 'w') as f:
        f.write(
            f'rest:\n'
            f'  - resource: http://homeassistant.local:8123/local/power_data.json\n'
            f'    sensor:\n'
        )
        for id in inverter_ids:
            panel_name = id.split('-')[0]  # Extract the panel name from the inverter ID
            f.write(
                f'      - name: "Solar Panel {panel_name} {id[-1]} power"\n'
                f'        value_template: \'{{{{ value_json["{id}"][0] }}}}\'\n'
                f'        unit_of_measurement: "W"\n\n'
                f'      - name: "Solar Panel {panel_name} {id[-1]} grid frequency"\n'
                f'        value_template: \'{{{{ value_json["{id}"][1] }}}}\'\n'
                f'        unit_of_measurement: "Hz"\n\n'
                f'      - name: "Solar Panel {panel_name} {id[-1]} grid voltage"\n'
                f'        value_template: \'{{{{ value_json["{id}"][2] }}}}\'\n'
                f'        unit_of_measurement: "V"\n\n'
                f'      - name: "Solar Panel {panel_name} {id[-1]} temperature"\n'
                f'        value_template: \'{{{{ value_json["{id}"][3] }}}}\'\n'
                f'        unit_of_measurement: "°C"\n\n'
            )

# Example usage with a web URL
#url = 'http://IP-OF-ECU-3/cgi-bin/parameters'
#url = 'http://IP-OF-ECU-4/index.php/realtimedata'
#url = 'http://example.com/ecu-data.html'
#generate_yaml(url)

# Example usage with a local file path
file_path_v4 = 'html-examples/ECU-v4.html'
generate_yaml(file_path_v4)
