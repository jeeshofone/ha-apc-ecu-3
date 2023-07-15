# this will read a cgi-bin script at http://IP-OF-ECU-3/cgi-bin/parameters and parse the output which is a table of values
# the values are then stored in a dictionary and the dictionary is returned to the calling program
# the calling program can then access the values by using the dictionary key
# the dictionary key is the name of the first column in the table named "Inverter ID"

# the columns in the table are as follows: Inverter ID, Current Power, Grid Frequency, Grid Voltage, Temperature, Date

# the following is an example of the output from the cgi-bin script
# <html><head><meta http-equiv=pragma content=no-cache><meta http-equiv=expire content=now><title></title></head><body bgcolor=ffffff text=black><br><br><table align=center border=1 cellpadding=0 cellspacing=0 bordercolor=#008000 bordercolorlight=#ffffff borderdark=#808000 width=1024><center><tr bgcolor=#43CD80><td align=center>Inverter ID</td><td align=center>Current Power</td><td align=center>Grid Frequency</td><td align=center>Grid Voltage</td><td align=center>Temperature</td><td align=center>Date</td></tr></center><center><tr><td align=center>404000058737-A</td><td align=center> 23&nbsp;W</td><td align=center> 50.0&nbsp;Hz</td><td align=center> 230&nbsp;V</td><td align=center> 45&nbsp;<sup>o</sup>C</td><td align=center> 2023-02-11 15:49:24</td></tr></center><center><tr><td align=center>404000058737-B</td><td align=center> 10&nbsp;W</td><td align=center> 50.0&nbsp;Hz</td><td align=center> 230&nbsp;V</td><td align=center> 45&nbsp;<sup>o</sup>C</td><td align=center> 2023-02-11 15:49:24</td></tr></center><center><tr><td align=center>404000060766-A</td><td align=center> 175&nbsp;W</td><td align=center> 50.0&nbsp;Hz</td><td align=center> 231&nbsp;V</td><td align=center> 50&nbsp;<sup>o</sup>C</td><td align=center> 2023-02-11 15:49:24</td></tr></center><center><tr><td align=center>404000060766-B</td><td align=center> 168&nbsp;W</td><td align=center> 50.0&nbsp;Hz</td><td align=center> 231&nbsp;V</td><td align=center> 50&nbsp;<sup>o</sup>C</td><td align=center> 2023-02-11 15:49:24</td></tr></center><center><tr><td align=center>404000060391-A</td><td align=center> 4&nbsp;W</td><td align=center> 50.0&nbsp;Hz</td><td align=center> 228&nbsp;V</td><td align=center> 43&nbsp;<sup>o</sup>C</td><td align=center> 2023-02-11 15:49:24</td></tr></center><center><tr><td align=center>404000060391-B</td><td align=center> 4&nbsp;W</td><td align=center> 50.0&nbsp;Hz</td><td align=center> 228&nbsp;V</td><td align=center> 43&nbsp;<sup>o</sup>C</td><td align=center> 2023-02-11 15:49:24</td></tr></center><center><tr><td align=center>404000060520-A</td><td align=center> 4&nbsp;W</td><td align=center> 50.0&nbsp;Hz</td><td align=center> 228&nbsp;V</td><td align=center> 40&nbsp;<sup>o</sup>C</td><td align=center> 2023-02-11 15:49:24</td></tr></center><center><tr><td align=center>404000060520-B</td><td align=center> 4&nbsp;W</td><td align=center> 50.0&nbsp;Hz</td><td align=center> 228&nbsp;V</td><td align=center> 40&nbsp;<sup>o</sup>C</td><td align=center> 2023-02-11 15:49:24</td></tr></center><center><tr><td align=center>404000060206-A</td><td align=center> 214&nbsp;W</td><td align=center> 50.0&nbsp;Hz</td><td align=center> 230&nbsp;V</td><td align=center> 56&nbsp;<sup>o</sup>C</td><td align=center> 2023-02-11 15:49:24</td></tr></center><center><tr><td align=center>404000060206-B</td><td align=center> 211&nbsp;W</td><td align=center> 50.0&nbsp;Hz</td><td align=center> 230&nbsp;V</td><td align=center> 56&nbsp;<sup>o</sup>C</td><td align=center> 2023-02-11 15:49:24</td></tr></center></table><br><br><hr></hr><center><tr><td>Greenstar Products Pty Ltd</td></tr></center></body></html>
# the output we care about in the html table will need to be parsed before it can be used

# the following is an example of the dictionary that is returned to the calling program
# {'404000058737-A': [' 23\xa0W', ' 50.0\xa0Hz', ' 230\xa0V', ' 45\xa0\xbaC', ' 2023-02-11 15:49:24'], '404000058737-B': [' 10\xa0W', ' 50.0\xa0Hz', ' 230\xa0V', ' 45\xa0\xbaC', ' 2023-02-11 15:49:24'], '404000060766-A': [' 175\xa0W', ' 50.0\xa0Hz', ' 231\xa0V', ' 50\xa0\xbaC', ' 2023-02-11 15:49:24'], '404000060766-B': [' 168\xa0W', ' 50.0\xa0Hz', ' 231\xa0V', ' 50\xa0\xbaC', ' 2023-02-11 15:49:24'], '404000060391-A': [' 4\xa0W', ' 50.0\xa0Hz', ' 228\xa0V', ' 43\xa0\xbaC', ' 2023-02-11 15:49:24'], '404000060391-B': [' 4\xa0W', ' 50.0\xa0Hz', ' 228\xa0V', ' 43\xa0\xbaC', ' 2023-02-11 15:49:24'], '404000060520-A': [' 4\xa0W', ' 50.0\xa0Hz', ' 228\xa0V', ' 40\xa0\xbaC', ' 2023-02-11 15:49:24'], '404000060520-B': [' 4\xa0W', ' 50.0\xa0Hz', ' 228\xa0V', ' 40\xa0\xbaC', ' 2023-02-11 15:49:24'], '404000060206-A': [' 214\xa0W', ' 50.0\xa0Hz', ' 230\xa0V', ' 56\xa0\xbaC', ' 2023-02-11 15:49:24'], '404000060206-B': [' 211\xa0


import requests
from bs4 import BeautifulSoup
import json

def get_power_data():
    # get the power data from the power meter - replace the IP address of your meter
    url = 'http://IP-OF-ECU-3/cgi-bin/parameters'
    r = requests.get(url)
    # check if the request was successful and print the output if the request failed then print the error and exit
    if r.status_code != 200:
        print('Error: ', r.status_code)
        exit()
    # parse the html output
    soup = BeautifulSoup(r.text, 'html.parser')
    # get the table that contains the power data
    table = soup.find('table')
    # print if we found a table or not
    if table is None:
        print('no table found')
    else:
        print('table found')   
    # get the rows of the table
    rows = table.find_all('tr')
    # create a dictionary to hold the power data
    power_data = {}
    # loop through the rows of the table
    for row in rows:
        # get how many columns are in the row
        columns = row.find_all('td')
        # if there are 6 columns then we have a row that contains power data
        if len(columns) == 6:
            # get the power data from the row
            power_data[columns[0].text] = [columns[1].text, columns[2].text, columns[3].text, columns[4].text, columns[5].text]
        else :
            # if there are not 6 columns then we have a row that does not contain power data
            print('not a power data row')
    # convert the special characters to normal characters
    # for each special character, replace it with the normal character
    for key in power_data:
        for i in range(len(power_data[key])):
            power_data[key][i] = power_data[key][i].replace('\xa0', ' ')
            power_data[key][i] = power_data[key][i].replace('\xba', ' ')
        power_data[key][0] = power_data[key][0].replace(' W', '')
        power_data[key][1] = power_data[key][1].replace(' Hz', '')
        power_data[key][2] = power_data[key][2].replace(' V', '')
        power_data[key][3] = power_data[key][3].replace(' oC', '')
    # save the power data dictionary to a json file
    with open('www/power_data.json', 'w') as outfile:
        json.dump(power_data, outfile)
    # close power_data.json file
    outfile.close()
"""     # remove the item in the json file that is indexed by "Inverter ID"
    with open('power_data.json', 'r') as f:
        data = json.load(f)
    del data['Inverter ID']
    with open('power_data.json', 'w') as f:
        json.dump(data, f)
    # close power_data.json file
    f.close() """


# call the function to get the power data
get_power_data()


# the following is a home assistant time pattern trigger to call this script every minute
# - platform: time_pattern
#   minutes: '/1'
#   seconds: '0'
#   timezone: 'America/New_York'
#   then:
#     - service: python_script.get_power_data
