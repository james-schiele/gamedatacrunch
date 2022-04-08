from asyncio.windows_events import INFINITE
from json.encoder import INFINITY
import requests
import pandas as pd
import json
from config.topgames.segmentations_gdc import *
import configparser
import math

config = configparser.RawConfigParser()
config.read("gamedatacrunch/config/topgames/gamedatacrunch_config.ini")

############################################################################################
#                                    Base Steam games                                      #
############################################################################################

top_100_performing_steam_games = []

def get_api_url():
    api_url = config.get("HTTP-ENDPOINT","GDC_API_URL_PREFIX")
    return api_url

def url_page(number):
    all_steam_games_url_suffix = config.get("HTTP-ENDPOINT", "GDC_API_URL_SUFFIX_ALL_GAMES")

    string = f'{number}{all_steam_games_url_suffix}'

    return string

def download_base():

    pages = 667 # hard-coded page number, max on today's site

    for page in range(665,pages):

        url = (get_api_url()+url_page(page)).replace('\"',"") # api for GameDataCrunch

        print(url)

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
    del df

if __name__ == "__main__":
    data = download_base()
