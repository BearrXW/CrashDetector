import time
import os
import psutil
import requests
import json
import subprocess
from datetime import datetime

# Discord webhook configuration
with open("webhook.txt", "r") as f:
    webhook_url = f.read().strip()

reopened_count = 0
checks_count = 0
last_restart_time = time.time()
message_id = None

# Set the restart interval and check interval
restart_interval = 20 * 60  # 20 minutes
check_interval = 5  # 5 seconds

# Logo
logo_color = '\033[92m'  # Green
logo = r"""
{logo_color}
   _____               _       _____       _            _             
  / ____|             | |     |  __ \     | |          | |            
 | |     _ __ __ _ ___| |__   | |  | | ___| |_ ___  ___| |_ ___  _ __ 
 | |    | '__/ _` / __| '_ \  | |  | |/ _ \ __/ _ \/ __| __/ _ \| '__|
 | |____| | | (_| \__ \ | | | | |__| |  __/ ||  __/ (__| || (_) | |   
  \_____|_|  \__,_|___/_| |_| |_____/ \___|\__\___|\___|\__\___/|_|   

""".format(logo_color=logo_color)

os.system('cls')
print(logo)
print("\nTotal restarts: {reopened_count}")
print(f"Checks: {checks_count}")
print()
print("Made By BearXxX#1940")
print("\n")


def send_webhook_update():
    global message_id
    current_time = datetime.now().strftime("Today at %H:%M")
    webhook_data = {
        "embeds": [{
            "title": "Crash Detector",
            "description": "The program crash detector is running.",
            "color": 0x7FFF00,
            "fields": [
                {
                    "name": "Total Restarts",
                    "value": str(reopened_count),
                    "inline": True
                },
                {
                    "name": "Total Checks",
                    "value": str(checks_count),
                    "inline": True
                }
            ],
            "footer": {
                "text": f"Made by BearXxX#1940 | {current_time}"
            }
        }]
    }
    headers = {"Content-Type": "application/json"}

    if message_id is None:
        response = requests.post(webhook_url, json=webhook_data, headers=headers)
        if response.status_code == 200:
            message_id = response.json()["id"]
            print("Discord webhook sent successfully.")
        else:
            print("Error sending Discord webhook.")
    else:
        edit_url = f"{webhook_url}/messages/{message_id}"
        response = requests.patch(edit_url, json=webhook_data, headers=headers)
        if response.status_code == 200:
            print("Discord webhook updated successfully.")
        else:
            print("Error updating Discord webhook.")


# ...

GREEN_COLOR = '\033[91m'  # Red
RESET_COLOR = '\033[0m'   # Reset color (\033[0m)

# ...

while True:
    if time.time() - last_restart_time >= restart_interval:
        checks_count = 0
        for process in psutil.process_iter():
            if process.name() == 'python.exe' and process.pid != os.getpid():
                process.terminate()
        reopened_count += 1
        last_restart_time = time.time()
        os.system('cls')
        print(GREEN_COLOR + logo + RESET_COLOR)
        print("")
        print(f"{GREEN_COLOR}Total restarts: {reopened_count}{RESET_COLOR}")
        print(f"{GREEN_COLOR}Checks: {checks_count}{RESET_COLOR}")
        print(f"{GREEN_COLOR}Made By BearXxX#1940{RESET_COLOR}")
        print("")
        print("")
        send_webhook_update()
        time.sleep(5)

    for process in psutil.process_iter():
        if process.name() == 'python.exe' and 'main.py' in process.cmdline():
            break
    else:
        checks_count += 1
        last_restart_time = time.time()
        os.system('cls')
        print(GREEN_COLOR + logo + RESET_COLOR)
        print("")
        print(f"{GREEN_COLOR}Total restarts: {reopened_count}{RESET_COLOR}")
        print(f"{GREEN_COLOR}Checks: {checks_count}{RESET_COLOR}")
        print(f"{GREEN_COLOR}Made By BearXxX#1940{RESET_COLOR}")
        print("")
        print("")

        send_webhook_update()
        subprocess.Popen(['python', 'main.py'], cwd=os.path.dirname(os.path.abspath(__file__)), creationflags=subprocess.CREATE_NEW_CONSOLE)
        send_webhook_update()

    time.sleep(check_interval)
