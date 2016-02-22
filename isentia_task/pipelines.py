# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymongo
import logging

logger = logging.getLogger(__name__)

class IsentiaTaskPipeline(object):
    
    collection_name = 'isentia_items'
    
    def __init__(self, mongo_uri, mongo_db, check_before_insert):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db
        self.check_before_insert = check_before_insert
        
    def process_item(self, item, spider):
        return item

    @classmethod
    def from_crawler(cls, crawler): 
        return cls(
            mongo_uri = crawler.settings.get('MONGO_URI'),
            mongo_db = crawler.settings.get('MONGO_DATABASE'),
            check_before_insert = crawler.settings.get('DISTRIBUTE_SPIDER')
        )
    
    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri) 
        self.db = self.client[self.mongo_db]
        logger.info('open mongo: %s and database: %s', self.mongo_uri, self.mongo_db)
    
    def close_spider(self, spider): 
        logger.info('close mongo')
        self.client.close()
    
    def process_item(self, item, spider): 
        #If we deploy multiple spider to crawl the same website, check the link before insert into db.
        if self.check_before_insert:
            lc = self.db[self.collection_name].find({"link":item['link']}).count()
            if lc != 0:
                logger.debug('%s has been seen in db', item['link'])
                return item
                
        self.db[self.collection_name].insert(dict(item)) 
        return item