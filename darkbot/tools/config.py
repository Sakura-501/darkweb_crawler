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

        self.mysql_host=config["mysql"]["host"]
        self.mysql_port = int(config["mysql"]["port"])
        self.mysql_user = config["mysql"]["user"]
        self.mysql_password = config["mysql"]["password"]
        self.mysql_database = config["mysql"]["database"]
        self.mysql_charset = config["mysql"]["charset"]

        self.mongo_host=config["mongo"]["host"]
        self.mongo_port=config["mongo"]["port"]
        self.mongo_database=config["mongo"]["database"]

        self.first_websites_list=list(set(config["first_websites"]["onion_list"]))


