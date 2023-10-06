import requests
from bs4 import BeautifulSoup
from datetime import datetime
import json

def get_power_data():
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
    power_data = {}

    for row in rows:
        columns = row.find_all('td')
        if len(columns) == 6:
            data_list = [columns[i].text.replace('\xa0', ' ').replace('\xba', ' ') for i in range(1, 6)]
            power_data[columns[0].text] = data_list
        else :
            print('Not a power data row')

    # Clean the data
    latest_time = '0'
    for pannel in power_data:
        if pannel != 'Inverter ID':  # skip the row of headers
            # Remove units from the data
            power_data[pannel][0] = power_data[pannel][0].replace(' W', '')
            power_data[pannel][1] = power_data[pannel][1].replace(' Hz', '')
            power_data[pannel][2] = power_data[pannel][2].replace(' V', '')
            power_data[pannel][3] = power_data[pannel][3].replace(' oC', '')

            # Panels go offline at night and return empty values. Mark these as 0
            # instead to prevent the HA sensor from disappearing.
            power_data[pannel] = [d.strip() or '0' for d in power_data[pannel]]
            
            # Note the latest timestamp found so we can fill it in for missing
            # panels.
            latest_time = max(latest_time, power_data[pannel][4])
    # For missing panels (offline over night etc) fill in the latest timestamp
    # found. If all are offline, fill in the current time.
    if latest_time == '0':
        latest_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    for pannel in power_data:
        if power_data[pannel][4] == '0':
            power_data[pannel][4] = latest_time
        
    with open('www/power_data.json', 'w') as outfile:
        json.dump(power_data, outfile)

get_power_data()
