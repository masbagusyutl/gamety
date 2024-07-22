import requests
import json
import time
from datetime import datetime
import random

# Fungsi untuk memuat data dari file data.txt
def load_data(file_path):
    with open(file_path, 'r') as file:
        data = file.read().strip()
    return data

# Fungsi untuk mendapatkan token Authorization
def get_authorization_token(web_app_data):
    url = 'https://gamety-clicker-api.metafighter.com/api/v1/auth/'
    payload = {"web_app_data": web_app_data}
    headers = {
        "Content-Type": "application/json",
    }
    response = requests.post(url, headers=headers, data=json.dumps(payload))
    if response.status_code == 200:
        try:
            auth_data = response.json()
            return auth_data.get('token')
        except json.JSONDecodeError:
            print("Failed to parse authorization response.")
            return None
    else:
        print(f"Failed to get authorization token. Status code: {response.status_code}")
        return None

# Fungsi untuk mendapatkan data user dengan token Authorization
def get_user_data(auth_token):
    request_date = datetime.now().strftime('%Y-%m-%dT%H:%M:%S')
    url = f'https://gamety-clicker-api.metafighter.com/api/v1/user/?request_date={request_date}'
    headers = {
        "Authorization": f"Bearer {auth_token}",
        "Accept": "*/*",
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36 Edg/126.0.0.0",
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        print("User data retrieved successfully.")
        return response.json()
    else:
        print(f"Failed to get user data. Status code: {response.status_code}")
        return None

# Fungsi untuk melakukan klik
def perform_clicks(auth_token, url, defeat_url):
    total_clicks = 505
    clicks_done = 0
    while clicks_done < total_clicks:
        click_number = random.randint(10, 50)
        if clicks_done + click_number > total_clicks:
            click_number = total_clicks - clicks_done
        payload = {
            "click_number": str(click_number),
            "click_date": datetime.now().strftime('%Y-%m-%dT%H:%M:%S')
        }
        headers = {
            "Authorization": f"Bearer {auth_token}",
            "Accept": "*/*",
            "Content-Type": "application/json",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36 Edg/126.0.0.0",
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

# Fungsi utama
def main():
    web_app_data = load_data('data.txt')
    auth_token = get_authorization_token(web_app_data)
    if auth_token:
        user_data = get_user_data(auth_token)
        if user_data:
            print(user_data)
            # URL klik
            click_url = "https://gamety-clicker-api.metafighter.com/api/v1/actions/click/"
            # URL defeat (contoh)
            defeat_url = "https://gamety-clicker-api.metafighter.com/api/v1/actions/defeat/"
            perform_clicks(auth_token, click_url, defeat_url)

if __name__ == "__main__":
    main()
