import logging
import os
from getpass import getpass
from netmiko import ConnectHandler
from ntc_templates.parse import parse_output



print("LAB2_START")

logging.basicConfig(
    filename="logs/lab.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logging.info("LAB2_START")
print("[STEP 2] DEV Container Started")
logging.info("[STEP 2] DEV Container Started")

COMMANDS = [
    "show version",
    "show ip interface brief",
    "show inventory",
]

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW_DIR = os.path.join(BASE_DIR, "data", "raw")
REPORT_DIR = os.path.join(BASE_DIR, "reports")

os.makedirs(RAW_DIR, exist_ok=True)
os.makedirs(REPORT_DIR, exist_ok=True)

def collect_credentials():
    username = input("Enter username: ")
    password = getpass("Enter password: ")

    logging.info("CREDENTIALS_COLLECTED")

    return username, password

def connect_to_device(host, username, password):
    device = {
        "device_type": "cisco_ios",
        "host": host,
        "username": username,
        "password": password,
        "timeout": 10,
    }
    connection =ConnectHandler(**device)
    logging.info("CONNECT_OK")
    return connection

def run_commands(connection):
    outputs = {}

    for command in COMMANDS:
        output = connection.send_command(command)
        outputs[command] = output

        logging.info(f"CMD_RUN:{command}")

        filename = command.replace(" ", "_").replace("/", "_")
        filepath = os.path.join(RAW_DIR, f"{filename}.txt")

        with open(filepath, "w", encoding="utf-8") as file:
            file.write(output)

    return outputs

def parse_commands(outputs):
    parsed_outputs = {}

    for command, output in outputs.items():
        parsed = parse_output(
            platform="cisco_ios",
            command=command,
            data=output
        )

        parsed_outputs[command] = parsed

        logging.info(f"PARSE_OK:{command}")

    return parsed_outputs

def create_report(parsed_outputs):
    report_path = os.path.join(REPORT_DIR, "summary.txt")

    with open(report_path, "w", encoding="utf-8") as file:
        file.write("LAB 2 NETWORK DEVICE SUMMARY\n")
        file.write("============================\n\n")

        for command, data in parsed_outputs.items():
            file.write(f"Command: {command}\n")
            file.write(f"Records parsed: {len(data)}\n\n")

    logging.info("REPORT_SAVED")

def main():
    host = input("Enter device IP address: ")

    username, password = collect_credentials()

    connection = connect_to_device(
        host,
        username,
        password
    )

    try:
        outputs = run_commands(connection)
        parsed_outputs = parse_commands(outputs)
        create_report(parsed_outputs)
    finally:
        connection.disconnect()

if __name__ == "__main__":
      main()
logging.info("LAB2_END")
print("LAB2_END")




