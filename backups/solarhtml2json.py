# this will read a cgi-bin script at http://10.40.0.116/cgi-bin/parameters and parse the output which is a table of values
# the values are then stored in a dictionary and the dictionary is returned to the calling program
# the calling program can then access the values by using the dictionary key
# the dictionary key is the name of the first column in the table named "Inverter ID"

# the columns in the table are as follows: Inverter ID, Current Power, Grid Frequency, Grid Voltage, Temperature, Date

# the following is an example of the output from the cgi-bin script
# <html><head><meta http-equiv=pragma content=no-cache><meta http-equiv=expire content=now><title></title></head><body bgcolor=ffffff text=black><br><br><table align=center border=1 cellpadding=0 cellspacing=0 bordercolor=#008000 bordercolorlight=#ffffff borderdark=#808000 width=1024><center><tr bgcolor=#43CD80><td align=center>Inverter ID</td><td align=center>Current Power</td><td align=center>Grid Frequency</td><td align=center>Grid Voltage</td><td align=center>Temperature</td><td align=center>Date</td></tr></center><center><tr><td align=center>404000058737-A</td><td align=center> 23&nbsp;W</td><td align=center> 50.0&nbsp;Hz</td><td align=center> 230&nbsp;V</td><td align=center> 45&nbsp;<sup>o</sup>C</td><td align=center> 2023-02-11 15:49:24</td></tr></center><center><tr><td align=center>404000058737-B</td><td align=center> 10&nbsp;W</td><td align=center> 50.0&nbsp;Hz</td><td align=center> 230&nbsp;V</td><td align=center> 45&nbsp;<sup>o</sup>C</td><td align=center> 2023-02-11 15:49:24</td></tr></center><center><tr><td align=center>404000060766-A</td><td align=center> 175&nbsp;W</td><td align=center> 50.0&nbsp;Hz</td><td align=center> 231&nbsp;V</td><td align=center> 50&nbsp;<sup>o</sup>C</td><td align=center> 2023-02-11 15:49:24</td></tr></center><center><tr><td align=center>404000060766-B</td><td align=center> 168&nbsp;W</td><td align=center> 50.0&nbsp;Hz</td><td align=center> 231&nbsp;V</td><td align=center> 50&nbsp;<sup>o</sup>C</td><td align=center> 2023-02-11 15:49:24</td></tr></center><center><tr><td align=center>404000060391-A</td><td align=center> 4&nbsp;W</td><td align=center> 50.0&nbsp;Hz</td><td align=center> 228&nbsp;V</td><td align=center> 43&nbsp;<sup>o</sup>C</td><td align=center> 2023-02-11 15:49:24</td></tr></center><center><tr><td align=center>404000060391-B</td><td align=center> 4&nbsp;W</td><td align=center> 50.0&nbsp;Hz</td><td align=center> 228&nbsp;V</td><td align=center> 43&nbsp;<sup>o</sup>C</td><td align=center> 2023-02-11 15:49:24</td></tr></center><center><tr><td align=center>404000060520-A</td><td align=center> 4&nbsp;W</td><td align=center> 50.0&nbsp;Hz</td><td align=center> 228&nbsp;V</td><td align=center> 40&nbsp;<sup>o</sup>C</td><td align=center> 2023-02-11 15:49:24</td></tr></center><center><tr><td align=center>404000060520-B</td><td align=center> 4&nbsp;W</td><td align=center> 50.0&nbsp;Hz</td><td align=center> 228&nbsp;V</td><td align=center> 40&nbsp;<sup>o</sup>C</td><td align=center> 2023-02-11 15:49:24</td></tr></center><center><tr><td align=center>404000060206-A</td><td align=center> 214&nbsp;W</td><td align=center> 50.0&nbsp;Hz</td><td align=center> 230&nbsp;V</td><td align=center> 56&nbsp;<sup>o</sup>C</td><td align=center> 2023-02-11 15:49:24</td></tr></center><center><tr><td align=center>404000060206-B</td><td align=center> 211&nbsp;W</td><td align=center> 50.0&nbsp;Hz</td><td align=center> 230&nbsp;V</td><td align=center> 56&nbsp;<sup>o</sup>C</td><td align=center> 2023-02-11 15:49:24</td></tr></center></table><br><br><hr></hr><center><tr><td>Greenstar Products Pty Ltd</td></tr></center></body></html>
# the output we care about in the html table will need to be parsed before it can be used

# the following is an example of the dictionary that is returned to the calling program
# {'404000058737-A': [' 23\xa0W', ' 50.0\xa0Hz', ' 230\xa0V', ' 45\xa0\xbaC', ' 2023-02-11 15:49:24'], '404000058737-B': [' 10\xa0W', ' 50.0\xa0Hz', ' 230\xa0V', ' 45\xa0\xbaC', ' 2023-02-11 15:49:24'], '404000060766-A': [' 175\xa0W', ' 50.0\xa0Hz', ' 231\xa0V', ' 50\xa0\xbaC', ' 2023-02-11 15:49:24'], '404000060766-B': [' 168\xa0W', ' 50.0\xa0Hz', ' 231\xa0V', ' 50\xa0\xbaC', ' 2023-02-11 15:49:24'], '404000060391-A': [' 4\xa0W', ' 50.0\xa0Hz', ' 228\xa0V', ' 43\xa0\xbaC', ' 2023-02-11 15:49:24'], '404000060391-B': [' 4\xa0W', ' 50.0\xa0Hz', ' 228\xa0V', ' 43\xa0\xbaC', ' 2023-02-11 15:49:24'], '404000060520-A': [' 4\xa0W', ' 50.0\xa0Hz', ' 228\xa0V', ' 40\xa0\xbaC', ' 2023-02-11 15:49:24'], '404000060520-B': [' 4\xa0W', ' 50.0\xa0Hz', ' 228\xa0V', ' 40\xa0\xbaC', ' 2023-02-11 15:49:24'], '404000060206-A': [' 214\xa0W', ' 50.0\xa0Hz', ' 230\xa0V', ' 56\xa0\xbaC', ' 2023-02-11 15:49:24'], '404000060206-B': [' 211\xa0

# the following is a home assistant time pattern trigger to call this script every minute
# - platform: time_pattern
#   minutes: '/1'
#   seconds: '0'
#   timezone: 'America/New_York'
#   then:
#     - service: python_script.get_power_data

import requests
from bs4 import BeautifulSoup
from datetime import datetime
import json

def get_power_data():
    url = 'http://10.40.0.235/cgi-bin/parameters'
    #url = 'http://IP-OF-ECU-4/index.php/realtimedata'
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

    is_new_version = False
    for row in rows:
        columns = row.find_all('td')
        if len(columns) == 6:
            is_new_version = True
            break

    if is_new_version:
        inverter_id = None
        for row in rows[1:]:  # Skip the header row
            columns = row.find_all('td')
            if len(columns) == 6:
                inverter_id = columns[0].text.strip()
                power_data[inverter_id] = [columns[i].text.replace('&#176;C', '').strip() for i in range(1, 6)]
            else:
                power_data[inverter_id][0] += f" / {columns[1].text.strip()}"
                power_data[inverter_id][2] += f" / {columns[3].text.strip()}"
    else:
        for row in rows:
            columns = row.find_all('td')
            if len(columns) == 6:
                data_list = [columns[i].text.replace('\xa0', ' ').replace('\xba', ' ').strip() for i in range(1, 6)]
                power_data[columns[0].text.strip()] = data_list
            else:
                print('Not a power data row')

    # Clean the data
    latest_time = '0'
    for pannel in power_data:
        if pannel != 'Inverter ID':  # skip the row of headers
            # Remove units from the data
            if is_new_version:
                power_data[pannel][0] = power_data[pannel][0].replace('W', '').replace('/', '').strip()
                power_data[pannel][1] = power_data[pannel][1].replace('Hz', '').strip()
                power_data[pannel][2] = power_data[pannel][2].replace('V', '').replace('/', '').strip()
                power_data[pannel][3] = power_data[pannel][3].replace('°C', '').strip()
            else:
                power_data[pannel][0] = power_data[pannel][0].replace('W', '').strip()
                power_data[pannel][1] = power_data[pannel][1].replace('Hz', '').strip()
                power_data[pannel][2] = power_data[pannel][2].replace('V', '').strip()
                power_data[pannel][3] = power_data[pannel][3].replace('oC', '').strip()

            # Panels go offline at night and return empty values. Mark these as 0
            # instead to prevent the HA sensor from disappearing.
            power_data[pannel] = ['0' if d.strip() in ['', '-'] else d.strip() for d in power_data[pannel]]

            # Note the latest timestamp found so we can fill it in for missing
            # panels.
            latest_time = max(latest_time, power_data[pannel][4])

    # For missing panels (offline over night etc) fill in the latest timestamp
    # found. If all are offline, fill in the current time.
    if latest_time == '0':
        latest_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    for pannel in power_data:
        if power_data[pannel][4] == '0':
            power_data[pannel][4] = latest_time

    with open('www/power_data.json', 'w') as outfile:
        json.dump(power_data, outfile)

get_power_data()