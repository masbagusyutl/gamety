import requests
import json
import random
import time
from datetime import datetime, timedelta

def load_authorizations(file_path):
    with open(file_path, 'r') as f:
        return [line.strip() for line in f]

def get_current_time():
    return datetime.now().strftime('%Y-%m-%dT%H:%M:%S')

def perform_defeat(auth_token, url, attempts=3):
    for attempt in range(attempts):
        click_number = random.randint(1, 3)
        payload = {
            "click_number": str(click_number),
            "click_date": get_current_time()
        }
        headers = {
            "Authorization": f"Bearer {auth_token}",
            "Accept": "*/*",
            "Content-Type": "application/json",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36 Edg/126.0.0.0",
            # Add other headers here if needed
        }
        response = requests.post(url, headers=headers, data=json.dumps(payload))
        if response.status_code == 200:
            print(f"Successfully sent {click_number} defeats (attempt {attempt+1}).")
        else:
            print(f"Failed to send defeats on attempt {attempt+1}. Status code: {response.status_code}")
            return False
        time.sleep(5)  # Delay between requests
    return True

def perform_clicks(auth_token, url, defeat_url):
    total_clicks = 505
    clicks_done = 0
    while clicks_done < total_clicks:
        click_number = random.randint(10, 50)
        if clicks_done + click_number > total_clicks:
            click_number = total_clicks - clicks_done
        payload = {
            "click_number": str(click_number),
            "click_date": get_current_time()
        }
        headers = {
            "Authorization": f"Bearer {auth_token}",
            "Accept": "*/*",
            "Content-Type": "application/json",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36 Edg/126.0.0.0",
            # Add other headers here if needed
        }
        response = requests.post(url, headers=headers, data=json.dumps(payload))
        if response.status_code == 200:
            print(f"Successfully sent {click_number} clicks.")
            clicks_done += click_number
        elif response.status_code == 401:
            print("Authorization failed, performing defeat tasks.")
            if perform_defeat(auth_token, defeat_url):
                print("Defeat tasks completed successfully.")
            else:
                print("Defeat tasks failed.")
            break
        else:
            print(f"Failed to send clicks. Status code: {response.status_code}")
        time.sleep(5)  # Delay between requests

def countdown_and_restart():
    while True:
        end_time = datetime.now() + timedelta(hours=14)
        while datetime.now() < end_time:
            remaining_time = end_time - datetime.now()
            print(f"Time remaining: {str(remaining_time).split('.')[0]}", end='\r')
            time.sleep(1)
        print("\nRestarting script...")
        main()  # Restart the script

def main():
    click_url = 'https://gamety-clicker-api.metafighter.com/api/v1/actions/click/'
    defeat_url = 'https://gamety-clicker-api.metafighter.com/api/v1/actions/defeat/'
    auth_tokens = load_authorizations('data.txt')
    num_accounts = len(auth_tokens)
    for i, auth_token in enumerate(auth_tokens):
        print(f"Processing account {i+1}/{num_accounts}")
        perform_clicks(auth_token, click_url, defeat_url)
        print(f"Finished processing account {i+1}/{num_accounts}")
        time.sleep(5)  # Delay between accounts
    countdown_and_restart()

if __name__ == "__main__":
    main()
