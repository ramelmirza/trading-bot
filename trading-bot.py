import os
import requests
import json
import csv

"""
Date: 16-01-2025
Version: 1.00
"""


def get_request():
    """
    Sends a GET request to CoinMarketCap's API
    :return: JSON string converted to a dict, else return None
    """
    private_api_key = ""
    url = "https://pro-api.coinmarketcap.com/v2/cryptocurrency/quotes/latest"
    query_params = {"CMC_PRO_API_KEY": private_api_key, "id": 1}

    try:
        response = requests.get(url, params=query_params)
        if response.status_code == 200:
            json_data = json.loads(response.content)
            return json_data
        else:
            print(f"ERROR: {url} | STATUS: {response.status_code}")
    except requests.RequestException as re:
        print(f"ERROR: {url} | {re}")


def json_to_csv():
    """
    Converts JSON string/dict to CSV for future data manipulation (data retrieving/cleaning for now)
    :return: 1 if successful, None if not
    """
    file_name = "btc.csv"
    exists = os.path.exists(file_name)
    json_dict = get_request()

    if json_dict:
        json_dict = json_dict['data']['1']['quote']['USD']
        btc_data = {
            "price": round((json_dict["price"]), 2),
            "volume_24h": int((json_dict["volume_24h"])),
            "percent_change_24h": json_dict["percent_change_24h"],
            "market_cap": int((json_dict["market_cap"])),
            "market_cap_dominance": json_dict["market_cap_dominance"],
            "date": json_dict["last_updated"]
        }

        if exists:
            file_mode = 'a'
            print("Appending data to btc.csv--")
        else:
            file_mode = 'w'
            print("Writing data to btc.csv--")

        with open(file_name, file_mode, newline='') as csv_file:
            writer = csv.writer(csv_file)
            if file_mode == 'a':  # already has csv header
                writer.writerow(btc_data.values())
                return 1
            elif file_mode == 'w':
                writer.writerow(btc_data.keys())
                writer.writerow(btc_data.values())

    else:
        print("Failed to retrieve GET request")
        return None


json_to_csv()