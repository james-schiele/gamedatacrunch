import configparser
import requests
import json
import pandas as pd

############################################################################################
#                                       Technologies                                       #
############################################################################################

unity_games = []

config = configparser.RawConfigParser()

config.read("gamedatacrunch/config/topgames/gamedatacrunch_config.ini")

def get_api_url():
    api_url = config.get("HTTP-ENDPOINT","GDC_API_URL_PREFIX")
    return api_url

def url_page(number):
    all_steam_games_url_suffix_1 = config.get("HTTP-ENDPOINT", "TECHNAMES_API_1")
    all_steam_games_url_suffix_2 = config.get("HTTP-ENDPOINT", "TECHNAMES_API_2")

    string = f'{number}{all_steam_games_url_suffix_1}{all_steam_games_url_suffix_2}'

    return string

def download_base():

    pages = 1000 # hard-coded page number, max on today's site

    for page in range(pages):

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

            unity_games.append(i)

        print("Page ", page, " ingested")

    df = pd.DataFrame.from_records(unity_games)
    gdc_pull = df.to_csv('gdc_top_steam_pull.csv')
    del df

if __name__ == "__main__":
    data = download_base()