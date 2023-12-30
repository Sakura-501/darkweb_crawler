import datetime

import httpx, re
from bs4 import BeautifulSoup
from tools.config import config_all
from tools.create_mongo import mongo_latest

config_all = config_all()
onion_list_collection_name = config_all.mongo_onion_list_collection_name
onion_content_collection_name = config_all.mongo_onion_content_collection_name
mongo_instance = mongo_latest()
db = mongo_instance.db

def insert_onion_content(url, crawl_time, status, title, head, body):
    now_collection = db[onion_content_collection_name]
    insert_data = {"url": url, "crawl_time": crawl_time, "status": status, "title": title, "head": head, "body": body}
    now_collection.insert_one(insert_data)

# 有去重
def insert_onion_list(source,url,crawl_time):
    now_collection = db[onion_list_collection_name]
    find_data = {"url":url}
    if now_collection.find_one(find_data) is None:
        insert_data = {"source":source,"url":url,"crawl_time":crawl_time}
        now_collection.insert_one(insert_data)

def grep_title_head_body_onion(text):
    result_of_onion = []
    soup = BeautifulSoup(text, "html.parser")
    title=soup.title.prettify() if soup.find("title") else None
    head=soup.head.prettify() if soup.find("head") else None
    body=soup.body.prettify() if soup.find("body") else None

    # 正则匹配onion域名
    # onion_url_pattern = r"https?://[^\s)(,'\"]+.onion"
    onion_url_pattern = r"[\w]{16}.onion|[\w]{56}.onion"
    result_of_onion = list(set(re.findall(onion_url_pattern, text,re.IGNORECASE|re.MULTILINE)))
    # print(result_of_onion)

    return title, head, body, result_of_onion


def crawl_and_get_collection_all_data(client: httpx.Client, seed):
    result_of_onion = []
    url= seed
    try:
        resp = client.get(url)
        status = resp.status_code
        if status == 200:
            title, head, body, result_of_onion = grep_title_head_body_onion(resp.text)
        else:
            title, head, body, result_of_onion = None, None, None, None
    except:
        status,title, head, body, result_of_onion = None, None, None, None,None

    return url,  status, title, head, body, result_of_onion


def run_websites_list(client: httpx.Client):
    onion_seed_list = config_all.first_websites_list
    print("All_onion_seed_list: " + str(onion_seed_list))

    # 根据初始的种子列表网站爬取onion域名
    for i in range(len(onion_seed_list)):
        seed = onion_seed_list[i]
        print("{}.Get onions in {}".format(i + 1, seed))
        url,  status, title, head, body, result_of_onion = crawl_and_get_collection_all_data(client, seed)
        current_time = datetime.datetime.now()
        print("{} has {} onions".format(seed,len(result_of_onion)))

        # 1.先把现在这个seed插入到onion_list，source和url都是自己(这里需要先查询是否已存在url)
        insert_onion_list(seed, seed,current_time)
        # 2.先把初始种子网站获取的内容插入到onion_content集合中(这里直接插入，不需要查询)
        insert_onion_content(url, current_time, status, title, head, body)
        # 3.然后把从初始种子网站获取到的onion域名插入到onion_list集合中(这里需要先查询是否已存在url)
        for tmp_onion in result_of_onion:
            tmp_url1="http://"+tmp_onion
            insert_onion_list(seed,tmp_url1,current_time)
            tmp_url2="https://"+tmp_onion
            insert_onion_list(seed, tmp_url2, current_time)

        print("Done and next one!\n")


