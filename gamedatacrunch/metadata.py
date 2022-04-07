from asyncio.windows_events import INFINITE
from email import header
from json.encoder import INFINITY
import requests
import pandas as pd
import json
from config.topgames.segmentations import *
from config.topgames.test_pull_for_released_filter import url_sdk_playfab, test_url_page

metadata_json = []

df_metadata = ['TK_Number',
'Technology']

def get_api_endpoint_url():
    api_endpoint = "https://www.gamedatacrunch.com/api/steam/list/all/00/reviews_total?count=100&page=0&filters=re_out,ea_cur,tk160,tk205&filters_not=&sort_dir=-1"
    return api_endpoint

def download_base():

    url = get_api_endpoint_url()

    print(url)

    response = requests.get(url=url)

    if response.ok:
        data = response.json()
        json_data = json.loads(response.text)
    else:
        print("All pages ingested")

    metadata_json.append(json_data["techNames"])

if __name__ == "__main__":
    json_data = download_base()
    
    df = pd.DataFrame.from_records(metadata_json)

    df.insert(loc=0, column="TK_Name", value="TECH:NAME")

    metadata = df.to_csv('gdc_metadata.csv', index=False)

    df_unpivoted = df.melt(id_vars=["TK_Name"], var_name='TK_No.', value_name='Tester')

    df_unpivoted.to_csv('gdc_metadata.csv', index=False)
    
    # df_unpivoted[['Name','Type']] = df_unpivoted['Tester'].str.split(':',expand=True)

    namestypes = []

    for i in df_unpivoted['Tester']:
        namestypes.append(i)

print(namestypes[0])