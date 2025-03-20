# Device Automation with Python  and Netmiko

This project is a practical demonstration of how to automate common network administration tasks using **Python** and the powerful **Netmiko** library. It automates operations such as connecting to Cisco devices, restoring configurations from a backup, retrieving real-time system statistics (like CPU, memory usage, and interface traffic), and managing network interfaces. The result is an efficient, scalable solution for network device management.

## Prerequisites

To get started with this project, make sure you have the following:

- **Python 3.x** installed on your machine.
- The **Netmiko** library, which you can install via pip:
  
  ```bash
  pip install netmiko
  ```
  
- A **Cisco device (IOS XE)** with **SSH** enabled for remote access.
- A **backup configuration file** for restoring configurations (replaceable by your own file).

Once you have everything set up, you can use the script to automate various tasks and improve network management efficiency.

## Project Overview

The script provides functionality for:

- Connecting to a device over SSH.
- Restoring a device's configuration from a backup.
- Fetching device uptime, CPU/memory statistics, and interface traffic data.
- Enabling or disabling network interfaces.
- Retrieving the MAC address table of a device.

### Features

- **Logging:** Detailed logs of operations, including success and failure messages.
- **Error Handling:** Logs and manages exceptions to ensure smooth execution.
- **Real-Time Statistics:** Monitor traffic rates, device uptime, and resource usage.
- **Network Interface Management:** Easily enable or disable interfaces remotely.
  
The script provides a robust foundation for network automation tasks, reducing the need for manual intervention.

## Code Explanation


### 1. Importing Libraries
```python
import logging
from netmiko import ConnectHandler
import time
```
- **`logging`**: This built-in library is used to track the progress of the program. It captures key events, errors, and exceptions, and logs them for later analysis.
  
- **`ConnectHandler`** from **Netmiko**: This is the key library that enables the script to initiate an SSH connection to network devices (like Cisco routers and switches).
  
- **`time`**: Although not explicitly used in the current code, this module can be helpful for introducing time delays or timestamps in future modifications.

### 2. Configuring Logging
```python
logging.basicConfig(filename='device_automation.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
```
- This sets up logging to output logs to a file named `device_automation.log`. Logs include timestamps and log levels (e.g., `INFO`, `ERROR`), making it easier to trace the flow of execution and diagnose issues.

### 3. Device Connection Details
```python
ios_xe_device = {
    'device_type': 'cisco_ios',
    'host': '192.168.1.1',
    'username': 'your_username',
    'password': 'your_password',
    'secret': 'your_enable_password',
    'port': 22,
}
```
Here, you define the connection details for your Cisco device:

- **`device_type`**: Defines the type of device you're connecting to. In this case, it's a Cisco IOS device (`cisco_ios`).
- **`host`**: The IP address or hostname of the device.
- **`username`**: Your SSH username for logging in.
- **`password`**: The password associated with the username.
- **`secret`**: The enable password required to enter privileged EXEC mode.
- **`port`**: The SSH port to connect to (default is 22).

### 4. Establishing the SSH Connection
```python
def connect_to_device(device_info):
    """Establish SSH connection to the device."""
    try:
        net_connect = ConnectHandler(**device_info)
        net_connect.enable()
        logging.info("Successfully connected to the device.")
        return net_connect
    except Exception as e:
        logging.error(f"Error connecting to the device: {e}")
        return None
```
This function handles establishing an SSH connection to the device. If successful, it enters enable mode and logs a success message. If there is an issue (e.g., network problems, invalid credentials), it catches the exception and logs an error message.

### 5. Restoring Configuration from a Backup
```python
def restore_configuration(net_connect, backup_file):
    """Restore configuration from a backup file."""
    try:
        with open(backup_file, 'r') as file:
            config_commands = file.readlines()
        restore_output = net_connect.send_config_set(config_commands)
        logging.info("Configuration restored successfully.")
        return restore_output
    except Exception as e:
        logging.error(f"Error restoring configuration: {e}")
        return None
```
This function reads a backup configuration file, parses the commands, and sends them to the device to restore the configuration. It uses the `send_config_set()` method to push multiple configuration commands at once.

### 6. Fetching Device Uptime
```python
def check_device_uptime(net_connect):
    """Check the system uptime."""
    try:
        uptime_output = net_connect.send_command("show version | include uptime")
        logging.info("Fetched device uptime.")
        return uptime_output
    except Exception as e:
        logging.error(f"Error fetching uptime: {e}")
        return None
```
This function retrieves the system uptime by sending the command `show version | include uptime` to the device. It logs the result and any potential errors.

### 7. Monitoring Interface Traffic
```python
def monitor_interface_traffic(net_connect, interface):
    """Retrieve real-time traffic statistics for an interface."""
    try:
        command = f"show interfaces {interface} | include input rate|output rate"
        traffic_output = net_connect.send_command(command)
        logging.info(f"Fetched traffic statistics for {interface}.")
        return traffic_output
    except Exception as e:
        logging.error(f"Error retrieving traffic stats: {e}")
        return None
```
This function allows you to monitor the traffic on a specific network interface by executing the `show interfaces` command. It returns input and output traffic rates.

### 8. Toggling Interface State (Enable/Disable)
```python
def toggle_interface_state(net_connect, interface, enable=True):
    """Enable or disable a network interface."""
    try:
        command = [f"interface {interface}", "no shutdown" if enable else "shutdown"]
        toggle_output = net_connect.send_config_set(command)
        state = "enabled" if enable else "disabled"
        logging.info(f"Interface {interface} {state} successfully.")
        return toggle_output
    except Exception as e:
        logging.error(f"Error toggling interface state: {e}")
        return None
```
This function can enable or disable a specified network interface. It uses the `no shutdown` command to enable the interface and the `shutdown` command to disable it. The state change is logged for future reference.

### 9. Fetching the MAC Address Table
```python
def get_mac_address_table(net_connect):
    """Retrieve the MAC address table."""
    try:
        mac_table_output = net_connect.send_command("show mac address-table")
        logging.info("Fetched MAC address table.")
        return mac_table_output
    except Exception as e:
        logging.error(f"Error fetching MAC address table: {e}")
        return None
```
This function retrieves the MAC address table using the `show mac address-table` command, providing visibility into the MAC addresses learned by the switch.

### 10. Checking CPU and Memory Utilization
```python
def check_cpu_memory_usage(net_connect):
    """Check CPU and memory utilization."""
    try:
        cpu_output = net_connect.send_command("show processes cpu sorted | exclude 0.00%")
        memory_output = net_connect.send_command("show memory statistics")
        logging.info("Fetched CPU and memory usage.")
        return cpu_output, memory_output
    except Exception as e:
        logging.error(f"Error fetching CPU/memory usage: {e}")
        return None, None
```
This function checks the **CPU** and **memory** utilization of the device by executing the commands `show processes cpu sorted` and `show memory statistics`, respectively. The results are logged and returned for further use.

### 11. Main Execution Flow
```python
def main():
    net_connect = connect_to_device(ios_xe_device)
    if net_connect:
        print("Device Uptime:", check_device_uptime(net_connect))
        print("Traffic Stats:", monitor_interface_traffic(net_connect, "GigabitEthernet0/1"))
        print("MAC Address Table:", get_mac_address_table(net_connect))
        cpu, memory = check_cpu_memory_usage(net_connect)
        print("CPU Usage:\n", cpu)
        print("Memory Usage:\n", memory)
        close_connection(net_connect)
    else:
        print("Failed to connect to the device.")
```
This is the main function of the script. It establishes a connection to the device, retrieves various statistics, and prints them. If the connection fails, it displays an error message.

## Example Output

```text
Device Uptime: uptime is 10 weeks, 3 days, 12 hours, 25 minutes
Traffic Stats: GigabitEthernet0/1 input rate 5000 bits/sec, output rate 10000 bits/sec
MAC Address Table: 
Mac Address Table
----------------------
VLAN    MAC Address       Type       Ports
----    -----------       ----       -----
1       0015.63ab.1234    DYNAMIC    Gi0/1
CPU Usage:
%CPU usage details here
Memory Usage:
Memory stats details here
```

## Logging Example

The following logs will be generated during the execution:

```text
2025-03-20 10:05:22,356 - INFO - Successfully connected to the device.
2025-03-20 10:05:23,000 - INFO - Fetched device uptime.
2025-03-20 10:05:23,500 - INFO - Fetched traffic statistics for GigabitEthernet0/1.
2025-03-20 10:05:24,000 - INFO - Fetched MAC address table.
2025-03-20 10:05:25,000 - INFO - Fetched CPU and memory usage.
2025-03-20 10:05:26,000 - INFO - SSH connection closed.
```

## Conclusion

This script offers a comprehensive solution for automating network device management tasks. It facilitates essential operations such as monitoring device health, interface management, and configuration restoration. The power of **Netmiko** combined with **Python** makes this a scalable and efficient tool for network administrators and engineers.

---
