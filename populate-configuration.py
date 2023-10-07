import requests
from bs4 import BeautifulSoup

def generate_yaml():
    url = 'http://IP-OF-ECU-3/cgi-bin/parameters'
    r = requests.get(url)
    
    if r.status_code != 200:
        print('Error: ', r.status_code)
        return

    soup = BeautifulSoup(r.text, 'html.parser')
    table = soup.find('table')
    
    if table is None:
        print('No table found')
        return

    rows = table.find_all('tr')
    inverter_ids = []

    for i, row in enumerate(rows):
        columns = row.find_all('td')
        if len(columns) == 6:
            if i == 0:
                continue
            inverter_ids.append(columns[0].text)

    print(f'Found {len(inverter_ids)} inverters')

    with open('config_part.yaml', 'w') as f:
        f.write(
            f'rest:\n'
            f'  - resource: http://homeassistant.local:8123/local/power_data.json\n'
            f'    sensor:\n'
        )
        for i, id in enumerate(inverter_ids, start=1):
            f.write(
                f'      - name: "Solar Panel {str(i).zfill(2)} power"\n'
                f'        value_template: \'{{{{ value_json["{id}"][0] }}}}\'\n'
                f'        unit_of_measurement: "W"\n\n'
                f'      - name: "Solar Panel {str(i).zfill(2)} grid frequency"\n'
                f'        value_template: \'{{{{ value_json["{id}"][1] }}}}\'\n'
                f'        unit_of_measurement: "Hz"\n\n'
                f'      - name: "Solar Panel {str(i).zfill(2)} grid voltage"\n'
                f'        value_template: \'{{{{ value_json["{id}"][2] }}}}\'\n'
                f'        unit_of_measurement: "V"\n\n'
                f'      - name: "Solar Panel {str(i).zfill(2)} temperature"\n'
                f'        value_template: \'{{{{ value_json["{id}"][3] }}}}\'\n'
                f'        unit_of_measurement: "°C"\n\n'
            )

generate_yaml()