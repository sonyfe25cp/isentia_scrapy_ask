# -*- coding: utf-8 -*-

import web
import pymongo
import re
import logging

logger = logging.getLogger(__name__)

MONGO_URI = 'mongodb://isentia_chenjie:crawler_task@aws-us-east-1-portal.10.dblayer.com:10588,aws-us-east-1-portal.11.dblayer.com:27067'
MONGO_DB = 'isentia'
MONGO_COLLECTION = 'isentia_items'
cpc = pymongo.MongoClient(MONGO_URI)
mdb = cpc[MONGO_DB]
    

urls = (
    "/q/words=(.+)&begin=(\d+)&number=(\d+)", "q",
)
app = web.application(urls, globals())

class q:
    def GET(self, words, begin=0, number=10):
        items = []
        try:
            ip = web.ctx.env.get("ip")
            items = query(words.split(','), int(begin), int(number))
            logger.info('%s query [%s], return %s results', ip, words, len(items))
        except Exception, e:
            logger.error('%s exception when querying', e)
            
        web.header('Content-Type', 'application/json')
        return items
        
def query(words, begin, number):
    print "search", words, "limit", begin, ",", number
    
    sql = fuzzy_query_by_pymongo(" ".join(words))
    items = mdb[MONGO_COLLECTION].find(sql).skip(begin).limit(number)
    
    results = []
    for item in items:
        results.append(item)
    return results
    
    
# generate the fuzzy sql regard keywords
def fuzzy_query_by_pymongo(keywords):
    sql = {'title':{'$in':map(re.compile,keywords.split())}, 'content':{'$in':map(re.compile,keywords.split())}}
    return sql
    
    
    
if __name__ == "__main__":
    app.run()