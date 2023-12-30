import datetime

import httpx, re
from bs4 import BeautifulSoup
from tools.config import config_all
from tools.create_mongo import mongo_latest
from first_websites_list.onion_crawler import crawl_and_get_collection_all_data,insert_onion_list,insert_onion_content

config_all = config_all()
onion_list_collection_name = config_all.mongo_onion_list_collection_name
onion_content_collection_name = config_all.mongo_onion_content_collection_name
mongo_instance = mongo_latest()
db = mongo_instance.db
def search_keywords_from_config(client: httpx.Client,keywords):
    for one_keyword in keywords:
        print(one_keyword)


def search_one_keyword(client: httpx.Client,one_keyword):
    print(one_keyword)