# -*- coding: utf-8 -*-
import unittest
from isentia_task.spiders.theguardian import clean_html

class SpiderUtilsTest(unittest.TestCase):
    def test_clean_html(self):
        raw_html = "<h1>Hello, world</h1>"
        text = clean_html(raw_html)
        self.assertEqual(u'# Hello, world', text)
        
if __name__ == "__main__":
    unittest.main()