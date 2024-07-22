import requests
import json
import time
import random
from datetime import datetime, timedelta
from urllib.parse import quote

def load_tgwebappdata(file_path):
    with open(file_path, 'r') as f:
        return [line.strip() for line in f]

def format_tgwebappdata(raw_data):
    base_url = 'https://dt49tlqaucy6e.cloudfront.net/Prod_Build/index.html?bot_username=GametyApp_bot#tgWebAppData='
    encoded_data = quote(raw_data)
    tgwebappdata_url = f"{base_url}{encoded_data}&tgWebAppVersion=7.6&tgWebAppPlatform=tdesktop&tgWebAppThemeParams=%7B\"accent_text_color\"%3A\"%236ab2f2\"%2C\"bg_color\"%3A\"%2317212b\"%2C\"button_color\"%3A\"%235288c1\"%2C\"button_text_color\"%3A\"%23ffffff\"%2C\"destructive_text_color\"%3A\"%23ec3942\"%2C\"header_bg_color\"%3A\"%2317212b\"%2C\"hint_color\"%3A\"%23708499\"%2C\"link_color\"%3A\"%236ab3f3\"%2C\"secondary_bg_color\"%3A\"%23232e3c\"%2C\"section_bg_color\"%3A\"%2317212b\"%2C\"section_header_text_color\"%3A\"%236ab3f3\"%2C\"section_separator_color\"%3A\"%23111921\"%2C\"subtitle_text_color\"%3A\"%23708499\"%2C\"text_color\"%3A\"%23f5f5f5\"%7D"
    return tgwebappdata_url

def get_authorization(tgwebappdata_url):
    try:
        response = requests.get(tgwebappdata_url)
        response.raise_for_status()  # Raise an error for bad status codes
        auth_data = response.json()
        return auth_data.get('authorization')
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except requests.exceptions.RequestException as req_err:
        print(f"Request error occurred: {req_err}")
    except json.decoder.JSONDecodeError as json_err:
        print(f"JSON decode error: {json_err}")
        print(f"Response text: {response.text}")
    return None

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
    tgwebappdata_list = load_tgwebappdata('data.txt')
    num_accounts = len(tgwebappdata_list)
    for i, tgwebappdata in enumerate(tgwebappdata_list):
        print(f"Processing account {i+1}/{num_accounts}")
        tgwebappdata_url = format_tgwebappdata(tgwebappdata)
        print(f"Formatted URL: {tgwebappdata_url}")  # Debugging: print the formatted URL
        auth_token = get_authorization(tgwebappdata_url)
        if auth_token:
            perform_clicks(auth_token, click_url, defeat_url)
            print(f"Finished processing account {i+1}/{num_accounts}")
        else:
            print(f"Skipping account {i+1}/{num_accounts} due to authorization failure.")
        time.sleep(5)  # Delay between accounts
    countdown_and_restart()

if __name__ == "__main__":
    main()
