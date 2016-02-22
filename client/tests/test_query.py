# -*- coding: utf-8 -*-

import unittest
from query import QueryAPI
'''
Unit test about query api
'''
class QueryAPITest(unittest.TestCase):
    
    def test_connection(self):
        MONGO_URI = 'mongodb://a:b@192.168.1.1:27067'
        MONGO_DB = 'isentia'
        MONGO_COLLECTION = 'isentia_items'
        
        api = QueryAPI(MONGO_URI, MONGO_DB, MONGO_COLLECTION)
        (total, items) = api.query('a', 1, 2)
        api.close()
        self.assertEqual(0, total)
        self.assertEqual(0, len(items))
        
    def test_query(self):
        MONGO_URI = 'mongodb://isentia_chenjie:crawler_task@aws-us-east-1-portal.10.dblayer.com:10588,aws-us-east-1-portal.11.dblayer.com:27067'
        MONGO_DB = 'isentia'
        MONGO_COLLECTION = 'isentia_items'
        api = QueryAPI(MONGO_URI, MONGO_DB, MONGO_COLLECTION)
        (total, items) = api.query('China', 0, 2)
        api.close()
        self.assertEqual(2, len(items))
        
if __name__ == "__main__":
    unittest.main()