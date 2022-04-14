import requests
import pandas as pd
import json
# from config.topgames.test_pull_for_released_filter import url_sdk_playfab, test_url_page

metadata_json = []
types_list_dedupe = []
df_metadata = ['TK_Number','Technology']

def get_api_endpoint_url():
    api_endpoint = "https://www.gamedatacrunch.com/api/steam/list/all/00/reviews_total?count=100&page=0&filters=re_out,ea_cur,tk160,tk205&filters_not=&sort_dir=-1"
    return api_endpoint

def download_base():

    url = get_api_endpoint_url()

    print(url)

    response = requests.get(url=url)

    if response.ok:
        json_data = json.loads(response.text)
    else:
        print("All pages ingested")

    metadata_json.append(json_data["techNames"])

    return metadata_json

def sdk_engine_metadata_table(metadata_json):

    df = pd.DataFrame.from_records(metadata_json)
    df.insert(loc=0, column="TK_Name", value="TECH:NAME")

    df_unpivoted = df.melt(id_vars=["TK_Name"], var_name='TK_No.', value_name='Tester')
    
    namestypes = []

    for i in df_unpivoted['Tester']:
        namestypes.append(i)

        types_list = []

        type_ = []
        name_ = []

        for i in namestypes:
            for j in i:

                if j == 'type':
                    types_list.append(i[j])

                    print(i[j])

                if i[j] in (list(dict.fromkeys(types_list))):
                    type_.append(i[j])
                else:
                    name_.append(i[j])

    df_unpivoted['Type'] = pd.Series(type_)
    df_unpivoted['Name'] = pd.Series(name_)
    df_unpivoted = df_unpivoted.drop(columns=['Tester','TK_Name'])
    df_unpivoted.to_csv('gdc_technames_metadata.csv', index=False)

def technames_metadata_table():
    json_data = download_base()
    sdk_engine_metadata_table(json_data)

if __name__ == "__main__":

    json_data = download_base()
    sdk_engine_metadata_table(json_data)