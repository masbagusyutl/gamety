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

def login_and_get_access_token(web_app_data):
    url = 'https://gamety-clicker-api.metafighter.com/api/v1/auth/'
    payload = {
        "web_app_data": web_app_data
    }
    headers = {
        "Accept": "*/*",
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36 Edg/126.0.0.0"
    }
    response = requests.post(url, headers=headers, data=json.dumps(payload))
    if response.status_code == 200:
        tokens = response.json()
        return tokens['access']
    else:
        print(f"Login failed. Status code: {response.status_code}")
        return None

def get_account_info(auth_token):
    url = f'https://gamety-clicker-api.metafighter.com/api/v1/user/?request_date={get_current_time()}'
    headers = {
        "Authorization": f"Bearer {auth_token}",
        "Accept": "*/*",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36 Edg/126.0.0.0"
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        account_data = response.json()['data']
        print(f"telegram_id: {account_data['telegram_id']}")
        print(f"experience: {account_data['experience']}")
        print(f"coins: {account_data['coins']}")
        print(f"energy_current: {account_data['stat']['energy_current']}")
        print(f"energy_max: {account_data['stat']['energy_max']}")
    else:
        print(f"Failed to get account info. Status code: {response.status_code}")

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
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36 Edg/126.0.0.0"
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
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36 Edg/126.0.0.0"
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
    web_app_data_list = load_authorizations('data.txt')
    num_accounts = len(web_app_data_list)
    for i, web_app_data in enumerate(web_app_data_list):
        print(f"Processing account {i+1}/{num_accounts}")
        access_token = login_and_get_access_token(web_app_data)
        if access_token:
            get_account_info(access_token)
            perform_clicks(access_token, click_url, defeat_url)
        print(f"Finished processing account {i+1}/{num_accounts}")
        time.sleep(5)  # Delay between accounts
    countdown_and_restart()

if __name__ == "__main__":
    main()
