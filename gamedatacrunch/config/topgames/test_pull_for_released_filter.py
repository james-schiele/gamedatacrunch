from config.topgames.segmentations import api_url_address, api_steam_endpoint, api_top_performing_endpoint,api_page_number, NSFW
# import bs4, sys
# from urllib.request import urlopen
# from selenium import webdriver
# import time
import requests

# STAGES FOR INGESTING RELEASED STATUS

# 1 create api url 
# 2 iterate through pages
# 3 save json objects to list and convert to dataframe
# 4 do this for every "filter" type (see segmentations)
# 5 merge all dataframes to a base table of items and nest duplicate values using "Steamappid" as the unique identifier

def test_url_page(number):
    return f'/api/steam/list/all/reviews_total/?page={number}&field=title,release_date,price,base_price_usd,ea_status,review,reviews_total,unfiltered_reviews_total,peak_ccu,followers,playtracker_insight_rank,current_topsellers_rank,reviews_score_fancy,metacritic_score,opencritic_score,hidden_gem_score&sort_dir=-1'

# def filterd_page_test(number):
#     return f'https://www.gamedatacrunch.com/api/steam/list/all/00/reviews_total?count=100&page=0&filters=re_out,ea_cur,tk160&filters_not=&sort_dir=-1&cache=true'

def url_sdk_photon():
    return f'/api/steam/list/all/reviews_total?count=100&page=0&field=title,release_date,price,base_price_usd,ea_status,review,reviews_total,unfiltered_reviews_total,peak_ccu,followers,playtracker_insight_rank,current_topsellers_rank,reviews_score_fancy,metacritic_score,opencritic_score,hidden_gem_score&filters=tk160,tk238&filters_not=&sort_dir=-1&cache=true%27'

def url_sdk_discord():
    return f'/api/steam/list/all/reviews_total?count=100&page=0&field=title,release_date,price,base_price_usd,ea_status,review,reviews_total,unfiltered_reviews_total,peak_ccu,followers,playtracker_insight_rank,current_topsellers_rank,reviews_score_fancy,metacritic_score,opencritic_score,hidden_gem_score&filters=tk160,tk146&filters_not=&sort_dir=-1&cache=true%27'

def url_sdk_playfab():
    return f'/api/steam/list/all/reviews_total?count=100&page=0&field=title,release_date,price,base_price_usd,ea_status,review,reviews_total,unfiltered_reviews_total,peak_ccu,followers,playtracker_insight_rank,current_topsellers_rank,reviews_score_fancy,metacritic_score,opencritic_score,hidden_gem_score&filters=tk160,tk205&filters_not=&sort_dir=-1&cache=true%27'

# PAGE
def page_number(number):
    return '?page=1'
# [FILTERS]
api_filters_endpoint = "&filter="
# METHODS
def remove(string):
    return string.replace(" ", "")

Released_URLs = []

for key in NSFW:
    url = api_url_address+api_steam_endpoint+api_top_performing_endpoint + api_page_number +api_filters_endpoint+NSFW[key]
    # print(api_url_address+api_steam_endpoint+api_top_performing_endpoint+page_url+api_filters_endpoint+Released[key])
    # Released_URLs.append(api_url_address+api_steam_endpoint+api_top_performing_endpoint+api_filters_endpoint+Released[key])

def get_api_url():
    api_url = api_url_address+api_steam_endpoint+api_top_performing_endpoint+api_page_number+NSFW

    print(api_url)

def get_api_endpoints():
    endpoint = get_api_url()
    return endpoint

# ISSUES:

# The api endpoint does not repsond to changes in the url i.e. adding filters

# https://www.gamedatacrunch.com/api/steam/list/all/reviews_total/?field=title,release_date,price,ea_status,review,reviews_total&filter=tk145

# https://www.gamedatacrunch.com/api/steam/list/all/reviews_total/?field=title,release_date,price,ea_status,review,reviews_total&filter=tk145,tk141

# Both the above api endpoints return 65739 items without any filters despite them being included
