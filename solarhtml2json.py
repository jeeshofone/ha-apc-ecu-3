import requests
from bs4 import BeautifulSoup
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

    # Remove units from the data
    for key in power_data:
        power_data[key][0] = power_data[key][0].replace(' W', '')
        power_data[key][1] = power_data[key][1].replace(' Hz', '')
        power_data[key][2] = power_data[key][2].replace(' V', '')
        power_data[key][3] = power_data[key][3].replace(' oC', '')
        
    with open('www/power_data.json', 'w') as outfile:
        json.dump(power_data, outfile)

get_power_data()
