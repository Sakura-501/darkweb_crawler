import pymongo
from .config import config_all

config_all = config_all()


class mongo_latest:
    def __init__(self):
        mongo_url = "mongodb://{}:{}/".format(config_all.mongo_host, config_all.mongo_port)
        self.client = pymongo.MongoClient(mongo_url)
        self.db = self.client[config_all.mongo_database]

    # def create_onion_list_collection(self):
    #     collection_names=self.db.list_collection_names()
    #     if "onion_list" not in collection_names:
    #         tmp_collection=db["onion_list"]
