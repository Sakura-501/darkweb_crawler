import json
import os
from configparser import ConfigParser

class config_all:
    def __init__(self):
        config=ConfigParser()
        # 配置文件路径
        now_path=os.getcwd()
        config.read(now_path+"/config.ini",encoding="utf-8")
        # 详细配置
        self.tor_proxy_ip=config["tor"]["ip"]
        self.tor_proxy_port=config["tor"]["port"]
        self.tor_proxy = "socks5://{}:{}".format(self.tor_proxy_ip, self.tor_proxy_port)

        self.socks5_ip=config["socks5"]["ip"]
        self.socks5_port=config["socks5"]["port"]
        self.socks5_proxy="socks5://{}:{}".format(self.socks5_ip,self.socks5_port)

        # self.mysql_host=config["mysql"]["host"]
        # self.mysql_port = int(config["mysql"]["port"])
        # self.mysql_user = config["mysql"]["user"]
        # self.mysql_password = config["mysql"]["password"]
        # self.mysql_database = config["mysql"]["database"]
        # self.mysql_charset = config["mysql"]["charset"]

        self.mongo_host=config["mongo"]["host"]
        self.mongo_port=config["mongo"]["port"]
        self.mongo_database=config["mongo"]["database"]
        self.mongo_onion_list_collection_name=config["mongo"]["onion_list_collection_name"]
        self.mongo_onion_content_collection_name=config["mongo"]["onion_content_collection_name"]

        self.whether_crawl_again=config["setting"]["whether_crawl_again"]
        self.internal_time_to_crawl=int(config["setting"]["internal_time_to_crawl"])
        self.time_sleep_to_next_crawl=int(config["setting"]["time_sleep_to_next_crawl"])
        self.user_agents=list(set(json.loads(config["setting"]["user_agents"])))

        self.first_websites_list=list(set(json.loads(config["first_websites"]["onion_list"])))
        self.third_search_keywords=list(set(json.loads(config["third_search"]["keywords"])))
        self.fourth_tor2web_keywords=list(set(json.loads(config["fourth_tor2web"]["keywords"])))


