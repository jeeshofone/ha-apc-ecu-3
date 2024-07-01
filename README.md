# Home Assistant APC ECU-3 Data Reader

This custom component for Home Assistant fetches data from an APC ECU-3 or ECU-4 device and integrates it into your Home Assistant instance. It's currently a work in progress, but functional. You can find more information in this [blog post](https://www.123cloud.st/p/the-unexpectedly-direct-path-to-building).

## Requirements

- An APC ECU-3 or ECU-4 device connected to your network.
- The IP address of your APC ECU-3 or ECU-4 device.
- Home Assistant installation.

## Setup

### Creating a Virtual Python Environment on your Laptop/Desktop

0. **Clone the Repository**:
   ```bash
   git clone https://github.com/jeeshofone/ha-apc-ecu-3.git
   ```

2. **Install `virtualenv`**:
   ```bash
   pip install virtualenv
   ```

3. **Create a new virtual environment**:
   ```bash
   virtualenv venv
   ```

4. **Activate the virtual environment**:
   - On Windows:
     ```bash
     .\venv\Scripts\activate
     ```
   - On Unix or MacOS:
     ```bash
     source venv/bin/activate
     ```

5. **Install necessary dependencies**:

   Then install the dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Script Preparation

- Copy the `solarhtml2json.py` file to your Home Assistant configuration directory. This can be efficiently done using the File Editor add-on. The configuration directory’s default path is `/config`.

### Fetch and Save Power Data to create a template

- **From a Local HTML File (useful for testing)**:
  ```bash
  python /config/solarhtml2json.py --file path/to/your/file.html --ecu_v4  # for ECU v4
  python /config/solarhtml2json.py --file path/to/your/file.html  # for older versions (ECU-3)
  ```

- **From a URL**:
  ```bash
  python /config/solarhtml2json.py --url http://IP-OF-YOUR-DEVICE/index.php/realtimedata --ecu_v4  # for ECU v4
  python /config/solarhtml2json.py --url http://IP-OF-YOUR-DEVICE/cgi-bin/parameters  # for older versions (ECU-3)
  ```

### Generate Home Assistant Configuration

- After fetching the power data locally, generate the Home Assistant configuration part file:
  ```bash
  python /config/solarhtml2json.py --generate_config
  ```

- Add the contents of the generated `config_part.yaml` file to your `configuration.yaml` file in Home Assistant. You may need to combine your sensor section into any existing configurations. 

### Integration into Home Assistant

- Add a shell command in Home Assistant to automate data fetching:

  - **For ECU V4**:
    ```yaml
    shell_command:
      convert_solar_data: python /config/solarhtml2json.py --url http://IP-OF-YOUR-DEVICE/index.php/realtimedata --ecu_v4
    ```

  - **For ECU V3**:
    ```yaml
    shell_command:
      convert_solar_data: python /config/solarhtml2json.py --url http://IP-OF-YOUR-DEVICE/cgi-bin/parameters
    ```

- Create an automation to run the fetch command at your preferred frequency:
  ```yaml
  automation:
    - alias: get the solar data
      description: ""
      trigger:
        - platform: time_pattern
          minutes: "*"
          seconds: "0"
          hours: "*"
      condition: []
      action:
        - service: shell_command.convert_solar_data
          data: {}
      mode: single
  ```

## Usage

Once everything is set up, you will have the solar panel data from your APC ECU device available as sensor entities in Home Assistant. You can use these entities in your automations, dashboards, or any other feature within Home Assistant.

You will need to restart HomeAssistant for it to take in any new configuration changes.

The sensor names are based on the inverter IDs and are automatically generated by the script.

## Support and Contribution

This project is still under development, and your contributions are very welcome. If you encounter any issues or have suggestions, please open an issue on GitHub. If you can improve the code or add a feature, feel free to fork the repository and create a pull request.

