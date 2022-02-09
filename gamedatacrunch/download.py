from asyncio.windows_events import INFINITE
from json.encoder import INFINITY
import requests
import pandas as pd
import json
from config.topgames.segmentations import *
from config.topgames.test_pull_for_released_filter import test_url_page

top_100_performing_steam_games = []

def get_api_url():
    api_url = api_url_address
    return api_url


def get_api_endpoint():
    api_endpoint = api_top_performing_endpoint_all_fields
    return api_endpoint


def download_base():

    page = 658 # hard-coded page number, max on today's site

    for page in range(page, 665):

        url = get_api_url() + test_url_page(page) # api for GameDataCrunch

        response = requests.get(url=url)

        if response.ok:
            data = response.json()
            json_data = json.loads(response.text)
        else:
            print("All pages ingested")
            break

        for i in json_data['ranks']:

            top_100_performing_steam_games.append(i)

        print("Page ", page, " ingested")

        # return data

def download():

    page = 658

    for page in range(page, 665):

        url = get_api_url() + test_url_page(page)

        response = requests.get(url=url)

        if response.ok:
            data = response.json()
            json_data = json.loads(response.text)
        else:
            print("All pages ingested")
            break

        for i in json_data['ranks']:

            top_100_performing_steam_games.append(i)

        print("Page ", page, " ingested")

        # return data
            
print("File one __name__ is set to: {}" .format(__name__))

# create base table df

if __name__ == "__main__":
    data = download()
    df = pd.DataFrame.from_records(top_100_performing_steam_games)

    df["test_col"] = "test"
    test_csv = df.to_csv('testcsv.csv')