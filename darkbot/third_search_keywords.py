import httpx
from tools.config import config_all
from tools.create_mongo import mongo_latest
from first_websites_list import grep_title_head_body_onion, insert_onion_list

config_all = config_all()
onion_list_collection_name = config_all.mongo_onion_list_collection_name
onion_content_collection_name = config_all.mongo_onion_content_collection_name
mongo_instance = mongo_latest()
db = mongo_instance.db
search_url = "https://ahmia.fi/search/?q="
result_number=0


def search_keywords_from_config(client: httpx.Client, keywords):
    for one_keyword in keywords:
        search_one_keyword(client,one_keyword)


def search_one_keyword(client: httpx.Client, one_keyword):
    global result_number
    visit_url = search_url + one_keyword
    # print(visit_url)
    try:
        resp = client.get(url=visit_url)
        _, _, _, onion_result = grep_title_head_body_onion(resp.text)
        result_number += ((len(onion_result)) * 2)
        print("Has crawled onion_url: "+str(result_number))
        if onion_result is not None:
            for tmp_onion in onion_result:
                tmp_url1 = "http://" + tmp_onion
                insert_onion_list(visit_url, tmp_url1)
                tmp_url2 = "https://" + tmp_onion
                insert_onion_list(visit_url, tmp_url2)
    except Exception as e:
        print(e)


