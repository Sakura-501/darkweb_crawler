import datetime

import httpx, re
from bs4 import BeautifulSoup
from tools.config import config_all
from tools.create_mongo import mongo_latest
from first_websites_list import crawl_and_get_collection_all_data,insert_onion_list,insert_onion_content

config_all = config_all()
onion_list_collection_name = config_all.mongo_onion_list_collection_name
onion_content_collection_name = config_all.mongo_onion_content_collection_name
mongo_instance = mongo_latest()
db = mongo_instance.db

def get_all_onion_url():
    now_collection=db[str(onion_list_collection_name)]
    all_onion_url=now_collection.find({},{"url":1,"_id":0})
    return list(all_onion_url)

# 大于30天才重新访问
def check_repeat_content_and_internal_time(check_url):
    now_collection=db[onion_content_collection_name]
    if now_collection.find_one({"url":check_url}):
        res=now_collection.find({"url":check_url},{"crawl_time":1,"_id":0}).sort("crawl_time").limit(1)
        now_time=datetime.datetime.now()
        if (now_time-res[0]["crawl_time"]).days > config_all.internal_time_to_crawl:
            return False
    return True


def run_active_crawl(client: httpx.Client):
    print("start run_active_crawl!!!")
    already_crawl_onion_url = []
    while True:
        # 先拿到所有的onion_url
        prepare_all_onion_url=get_all_onion_url()

        # 循环跑，直到already和prepare数量相等，才停止
        if len(already_crawl_onion_url) == len(prepare_all_onion_url):
            break

        for one_url in prepare_all_onion_url:
            one_url=one_url["url"]
            if one_url not in already_crawl_onion_url:
                # 检查是否已经访问过了
                if check_repeat_content_and_internal_time(one_url):
                    current_time=datetime.datetime.now()
                    print(one_url+" is crawling!")
                    # 开始主动爬取并尝试匹配
                    url,  status, title, head, body, result_of_onion=crawl_and_get_collection_all_data(client,one_url)
                    # 插入content以及onion_list
                    insert_onion_content(url, current_time, status, title, head, body)
                    if result_of_onion is not None:
                        for tmp_onion in result_of_onion:
                            tmp_url1 = "http://" + tmp_onion
                            insert_onion_list(one_url, tmp_url1, current_time)
                            tmp_url2 = "https://" + tmp_onion
                            insert_onion_list(one_url, tmp_url2, current_time)
                else:
                    print(one_url+" has already crawled!")

                # 最后记得加入到已爬序列
                already_crawl_onion_url.append(one_url)



