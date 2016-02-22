# -*- coding: utf-8 -*-

from query import QueryAPI

MONGO_URI = 'mongodb://isentia_chenjie:crawler_task@aws-us-east-1-portal.10.dblayer.com:10588,aws-us-east-1-portal.11.dblayer.com:27067'
MONGO_DB = 'isentia'
MONGO_COLLECTION = 'isentia_items'
    
api = QueryAPI(MONGO_URI, MONGO_DB, MONGO_COLLECTION)

(total, items) = api.query('China', 0, 5)
for item in items:
    print item['title']