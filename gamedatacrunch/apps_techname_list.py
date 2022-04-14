from asyncio.windows_events import NULL
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
# Engine names & IDs
tk_ids_engine = []
tk_engine_names = []

# Engine dict
tk_dict_engine = []

# Engine dataframe
engine_tech_dfs = []

# SDK______________________________________________________________________________________#
#     
# SDK names & IDs
tk_ids_sdk = []
tk_sdk_names = []

# SDK dict
tk_dict_sdk = []

# SDK dataframe
sdk_tech_dfs = []


def retrieve_tk_id():
    
    with open('C:/Users/James Schiele/Documents/GitHub/gamedatacrunch/gdc_technames_metadata.csv', 'r') as csvfile:
        datareader = csv.reader(csvfile)
        next(datareader, None) 
        for row in datareader:
            if row[2] != 'Unknown':
                if row[1] == 'Engine':
                    tk_ids_engine.append(row[0])
                    tk_engine_names.append(row[2])

                    entry = {row[0]:row[2]}
                    print(entry)

                    tk_dict_engine.append(entry)
                
                if row[1] == 'SDK':
                    tk_ids_sdk.append(row[0])
                    tk_sdk_names.append(row[2])

                    entry = {row[0]:row[2]}

                    tk_dict_sdk.append(entry)

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

    for item in tk_dict_engine:

        for key, value in item.items():
            print(key,' and ',value)

        engine_games = []
        pages = 400

        for page in range(pages):

            url = (get_api_url()+url_page(page,key)).replace('\"',"") # api for GameDataCrunch

            response = requests.get(url=url)

            if response.ok:
                data = response.json()
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

        try:
            df = df[['steam_appid','Engine']]

            df = df.drop_duplicates()
            engine_tech_dfs.append(df)
            del df

            count += 1

        except:
            break

    for item in tk_dict_sdk:

        for key, value in item.items():
            print(key,' and ',value)

        sdk_games = []
        pages = 400

        for page in range(pages):

            url = (get_api_url()+url_page(page,key)).replace('\"',"") # api for GameDataCrunch

            response = requests.get(url=url)

            if response.ok:
                data = response.json()
                json_data = json.loads(response.text)
            else:
                print("All pages ingested")
                break

            for i in json_data['ranks']:
                sdk_games.append(i)

            print("Page ", page, " ingested")

        df = f'df_{value}'

        df = pd.DataFrame.from_records(sdk_games)
        df['SDK'] = value

        try:
            df = df[['steam_appid','SDK']]

            df = df.drop_duplicates()
            sdk_tech_dfs.append(df)
            # gdc_pull = df.to_csv(f'{value[1]}_games.csv', index=False)
            del df

            count += 1

        except:
            break

    
    sdk_df = pd.concat(sdk_tech_dfs).to_csv('gdc_steamids_sdk.csv', index=False)
    engine_df = pd.concat(engine_tech_dfs).to_csv('gdc_steamids_engines.csv', index=False)

def retrieve_engines_sdks_by_app_id():
    retrieve_tk_id()
    data = download_base()

if __name__ == "__main__":

    retrieve_tk_id()
    data = download_base()