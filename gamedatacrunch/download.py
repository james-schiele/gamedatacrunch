from asyncio.windows_events import INFINITE
from json.encoder import INFINITY
import requests
import pandas as pd
import json
from config.topgames.segmentations import *
from config.topgames.test_pull_for_released_filter import url_sdk_playfab, test_url_page

top_100_performing_steam_games = []

def get_api_url():
    api_url = api_url_address
    return api_url


def get_api_endpoint():
    api_endpoint = api_top_performing_endpoint_all_fields
    return api_endpoint


def download_base():

    pages = 1000 # hard-coded page number, max on today's site

    for page in range(pages):

        url = get_api_url() + test_url_page(page) # api for GameDataCrunch

        # print(url)

        response = requests.get(url=url)

        if response.ok:
            # data = response.json()
            json_data = json.loads(response.text)
        else:
            print("All pages ingested")
            break

        for i in json_data['ranks']:

            top_100_performing_steam_games.append(i)

        print("Page ", page, " ingested")

    df = pd.DataFrame.from_records(top_100_performing_steam_games)
    gdc_pull = df.to_csv('gdc_top_steam_pull.csv')


if __name__ == "__main__":
    data = download_base()
