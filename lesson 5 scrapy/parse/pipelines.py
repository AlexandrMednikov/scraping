# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from pymongo import MongoClient

class ParsePipeline:
    def __init__(self):
        client = MongoClient('localhost:27017')
        self.mongo_db = client.parse_mvideo

    def process_item(self, item, spider):
        # print(f"----------------------------\n{item}\n----------------------------")
        collection = self.mongo_db[spider.name]
        got = 0


        collection.insert_one(item)
