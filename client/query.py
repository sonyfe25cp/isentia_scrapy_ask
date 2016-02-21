# -*- coding: utf-8 -*-

import argparse
from optparse import OptionParser
import pymongo
import re
import logging

logger = logging.getLogger(__name__)

MONGO_URI = 'mongodb://isentia_chenjie:crawler_task@aws-us-east-1-portal.10.dblayer.com:10588,aws-us-east-1-portal.11.dblayer.com:27067'
MONGO_DB = 'isentia'
MONGO_COLLECTION = 'isentia_items'

def query(words, begin, number):
    
    print "search", words, "limit", begin, ",", number
    results = []
    total = 0
    cpc = pymongo.MongoClient(MONGO_URI)
    mdb = cpc[MONGO_DB]
    
    sql = fuzzy_query_by_pymongo(" ".join(words))
    try:
        items = mdb[MONGO_COLLECTION].find(sql).skip(begin).limit(number)
        total = items.count()
        for item in items:
            results.append(item)
    except Exception, e:
        logger.error('%e exception when querying', e)
    finally:
        cpc.close()
    return (total, results)
    
    
# generate the fuzzy sql regard keywords
def fuzzy_query_by_pymongo(keywords):
    sql = {'title':{'$in':map(re.compile,keywords.split())}, 'content':{'$in':map(re.compile,keywords.split())}}
    return sql
    
    
if __name__ == '__main__':
    from optparse import OptionParser
    optParser = OptionParser()
    optParser.add_option("-n","--number", type="int",dest = "number", help="the next n results, default 10", default = 10)
    optParser.add_option("-b","--begin", type="int",dest = "begin", help="the next n results, default 0", default = 0)
    options, args = optParser.parse_args()
    (total, items) = query(args, options.begin, options.number)
    
    print '**********There are', total, 'items related to the query**********'
    index = 1
    for item in items:
        print '*********Item num:', index, '**********'
        print item
        index += 1
    print '**********', len(items), 'items shown in the list**********'