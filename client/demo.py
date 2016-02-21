# -*- coding: utf-8 -*-

from query import query
items = query('China', 0, 5)
for item in items:
    print item['title']