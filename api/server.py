# -*- coding: utf-8 -*-

import web
import pymongo
import re
import logging
from client.query import QueryAPI

logger = logging.getLogger(__name__)

MONGO_URI = 'mongodb://isentia_chenjie:crawler_task@aws-us-east-1-portal.10.dblayer.com:10588,aws-us-east-1-portal.11.dblayer.com:27067'
MONGO_DB = 'isentia'
MONGO_COLLECTION = 'isentia_items'

api = QueryAPI(MONGO_URI, MONGO_DB, MONGO_COLLECTION)

urls = (
    "/q/words=(.+)&begin=(\d+)&number=(\d+)", "q",
)
app = web.application(urls, globals())

'''
the query function
'''
class q:
    def GET(self, words, begin=0, number=10):
        items = []
        try:
            ip = web.ctx.env.get("ip")
            (total, items) = api.query(words.split(','), int(begin), int(number))
            logger.info('%s query [%s], return %s results', ip, words, len(items))
        except Exception, e:
            logger.error('%s exception when querying', e)
            
        web.header('Content-Type', 'application/json')
        return items
    
    
if __name__ == "__main__":
    app.run()