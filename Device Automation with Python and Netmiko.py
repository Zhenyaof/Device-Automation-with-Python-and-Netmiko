import logging
from netmiko import ConnectHandler
import time

# Setup logging
logging.basicConfig(filename='device_automation.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Device information (replace with actual credentials)
ios_xe_device = {
    'device_type': 'cisco_ios',
    'host': '192.168.1.1',
    'username': 'your_username',
    'password': 'your_password',
    'secret': 'your_enable_password',
    'port': 22,
}

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

def check_device_uptime(net_connect):
    """Check the system uptime."""
    try:
        uptime_output = net_connect.send_command("show version | include uptime")
        logging.info("Fetched device uptime.")
        return uptime_output
    except Exception as e:
        logging.error(f"Error fetching uptime: {e}")
        return None

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

def get_mac_address_table(net_connect):
    """Retrieve the MAC address table."""
    try:
        mac_table_output = net_connect.send_command("show mac address-table")
        logging.info("Fetched MAC address table.")
        return mac_table_output
    except Exception as e:
        logging.error(f"Error fetching MAC address table: {e}")
        return None

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

def close_connection(net_connect):
    """Close the SSH connection."""
    try:
        net_connect.disconnect()
        logging.info("SSH connection closed.")
    except Exception as e:
        logging.error(f"Error closing the connection: {e}")

if __name__ == "__main__":
    main()
