import configparser
import requests
import json
import pandas as pd
import csv

config = configparser.RawConfigParser()
config.read("gamedatacrunch/config/topgames/gamedatacrunch_config.ini")

############################################################################################
#                                       Technologies                                       #
############################################################################################

# ENGINE___________________________________________________________________________________#
#                                                                                          #

tk_ids = []
tk_names = []

tk_dict = []

tech_dfs = []

def retrieve_tk_id():
    
    with open('C:/Users/James Schiele\Documents\GitHub\gamedatacrunch\gdc_technames_metadata.csv', 'r') as csvfile:
        datareader = csv.reader(csvfile)
        next(datareader, None) 
        for row in datareader:
            if row[1] == 'Engine':
                tk_ids.append(row[0])
                tk_names.append(row[2])

                entry = {row[0]:row[2]}

                tk_dict.append(entry)

def get_api_url():
    api_url = config.get("HTTP-ENDPOINT","GDC_API_URL_PREFIX")
    return api_url

def url_page(number, techid):
    all_steam_games_url_suffix_1 = config.get("HTTP-ENDPOINT", "TECHNAMES_API_1")
    all_steam_games_url_suffix_2 = config.get("HTTP-ENDPOINT", "TECHNAMES_API_2")

    string = f'{number}{all_steam_games_url_suffix_1},tk{techid}{all_steam_games_url_suffix_2}'

    return string

def download_base():

    count = 0

    for item in tk_dict:

        for key, value in item.items():
            print(key,' and ',value)

        engine_games = []
        pages = 1000

        for page in range(10):

            url = (get_api_url()+url_page(page,key)).replace('\"',"") # api for GameDataCrunch

            response = requests.get(url=url)

            if response.ok:
                # data = response.json()
                json_data = json.loads(response.text)
            else:
                print("All pages ingested")
                break

            for i in json_data['ranks']:
                engine_games.append(i)

            print("Page ", page, " ingested")

        df = f'df_{value}'

        df = pd.DataFrame.from_records(engine_games)
        df['Engine'] = value
        df = df[['steam_appid','Engine']]
        df = df.drop_duplicates()
        tech_dfs.append(df)
        gdc_pull = df.to_csv(f'{value[1]}_games.csv', index=False)
        del df

        count += 1
    
    final_df = pd.concat(tech_dfs).to_csv('final.csv', index=False)

if __name__ == "__main__":

    retrieve_tk_id()
    data = download_base()