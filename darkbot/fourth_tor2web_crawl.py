import time
import httpx,random
import re

from tools.create_mongo import mongo_latest
from tools.config import config_all
from first_websites_list import insert_onion_list


config_all=config_all()
sleep_time=config_all.time_sleep_to_next_crawl
tor2web_keywords=config_all.fourth_tor2web_keywords
onion_list_collection_name = config_all.mongo_onion_list_collection_name
onion_content_collection_name = config_all.mongo_onion_content_collection_name
mongo_instance = mongo_latest()
db = mongo_instance.db

def grep_tor2web_onion_result(text,one_keyword):
    result_of_onion = []
    # 正则匹配onion域名，然后添加.onion后缀
    # onion_url_pattern = r"https?://[^\s)(,'\"]+.onion"
    onion_url_pattern = fr"[\w]{{16}}.{one_keyword}|[\w]{{56}}.{one_keyword}"
    # print(onion_url_pattern)
    results = list(set(re.findall(onion_url_pattern, text,re.IGNORECASE|re.MULTILINE)))
    for tmp_result in results:
        result_of_onion.append(tmp_result.replace(one_keyword,"onion"))

    return result_of_onion

def insert_results_of_onion_to_collection(result_of_onion,real_url):
    for one_onion in result_of_onion:
        tmp_url1 = "http://" + one_onion
        insert_onion_list(real_url, tmp_url1)
        tmp_url2 = "https://" + one_onion
        insert_onion_list(real_url, tmp_url2)

def google_search_tor2web_keyword(one_keyword):
    print(f"google search_keyword: {one_keyword}")
    result_of_onion=[]
    # for i in range(1,10,10):
    for i in range(1,1000,10):
        # https://www.google.com/search?q=site:onion.to&start=1
        real_url="https://www.google.com/search?q=site:{}&start={}".format(one_keyword,str(i))
        headers = {"User-Agent": random.choice(config_all.user_agents)}
        # client = httpx.Client(proxies=config_all.socks5h_proxy, timeout=15, headers=headers, follow_redirects=True, verify=False)
        client = httpx.Client(timeout=15, headers=headers, follow_redirects=False, verify=False)
        try:
            resp=client.get(real_url)
            tmp_result=grep_tor2web_onion_result(resp.text,one_keyword)
            result_of_onion.extend(tmp_result)
            # print(result_of_onion)
            insert_results_of_onion_to_collection(tmp_result,real_url)
        except Exception as e:
            print(e)
        client.close()
        time.sleep(30)
    return list(set(result_of_onion))

# 我超，lite居然可以！！！
def duckduckgo_search_tor2web_keyword(one_keyword):
    print(f"duckduckgo search_keyword: {one_keyword}")
    result_of_onion=[]
    duckduckgo_url="https://lite.duckduckgo.com/lite/"
    for i in range(1,10,50):
        data={"q":f"site:{one_keyword}","dc":f"{i}","s":"50","kl":"wt-wt","o":"json"}
        headers = {"User-Agent": random.choice(config_all.user_agents)}
        client = httpx.Client(timeout=15, headers=headers, follow_redirects=False, verify=False)
        try:
            resp=client.post(duckduckgo_url,data=data)
            result_of_onion.extend(grep_tor2web_onion_result(resp.text,one_keyword))
        except Exception as e:
            print(e)
        client.close()
        time.sleep(30)

    result_of_onion=list(set(result_of_onion))
    insert_results_of_onion_to_collection(result_of_onion,duckduckgo_url+one_keyword)
    return result_of_onion

# 首页为6个，第二页从第7个开始，每页10个
def bing_search_tor2web_keyword(one_keyword):
    print(f"bing search_keyword: {one_keyword}")
    result_of_onion = []
    # 第一页
    bing_url=f"https://www.bing.com/search?q=site:{one_keyword}&first=1"
    headers = {"User-Agent": random.choice(config_all.user_agents)}
    client = httpx.Client(timeout=15, headers=headers, follow_redirects=False, verify=False)
    resp=client.get(bing_url)
    result_of_onion.extend(grep_tor2web_onion_result(resp.text,one_keyword))
    insert_results_of_onion_to_collection(result_of_onion, bing_url)
    client.close()
    # 第二页开始
    for i in range(7,1000,10):
        bing_url = f"https://www.bing.com/search?q=site:{one_keyword}&first={i}"
        headers = {"User-Agent": random.choice(config_all.user_agents)}
        client = httpx.Client( timeout=15, headers=headers, follow_redirects=False,
                              verify=False)
        try:
            resp = client.get(bing_url)
            tmp_result=grep_tor2web_onion_result(resp.text,one_keyword)
            result_of_onion.extend(tmp_result)
            insert_results_of_onion_to_collection(tmp_result,bing_url)
        except Exception as e:
            print(e)
        client.close()
        time.sleep(30)

    return list(set(result_of_onion))


def run_tor2web_crawl():
    print("start running tor2web_keywords_crawl!!!")
    google_result_of_onion=[]
    duckduckgo_result_of_onion=[]
    bing_result_of_onion=[]
    for one_keyword in tor2web_keywords:
        print(f"start search tor2web_keywords: {one_keyword}")

        google_result_of_onion.extend(google_search_tor2web_keyword(one_keyword))
        print(google_result_of_onion)
        duckduckgo_result_of_onion.extend(duckduckgo_search_tor2web_keyword(one_keyword))
        print(duckduckgo_result_of_onion)
        bing_result_of_onion.extend(bing_search_tor2web_keyword(one_keyword))
        print(bing_result_of_onion)

        time.sleep(10)

    google_result_of_onion=list(set(google_result_of_onion))
    print("google_length: "+str(len(google_result_of_onion)))
    duckduckgo_result_of_onion=list(set(duckduckgo_result_of_onion))
    print("duckduckgo_length: "+str(len(duckduckgo_result_of_onion)))
    bing_result_of_onion=list(set(bing_result_of_onion))
    print("bing_length: "+str(len(bing_result_of_onion)))
