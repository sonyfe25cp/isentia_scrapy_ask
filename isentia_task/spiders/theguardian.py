# -*- coding: utf-8 -*-
import scrapy
import re
from scrapy.selector import Selector
from isentia_task.items import IsentiaTaskItem

class TheguardianSpider(scrapy.Spider):
    
    name = "theguardian"
    allowed_domains = ["theguardian.com"]
    start_urls = (
        'http://www.theguardian.com/au',
    )

    #Parse the portal page
    def parse(self, response):        
        for href in response.xpath('//a/@href').extract():
            url = response.urljoin(href)
            
            #In the theguardian.com site, all the end page's url contains a year number.
            #This can be used as a tricky to recongize which url should be download and which should be follow.
            m = re.search(r'/\d{4}/', url)
            if m :
                #print 'download this link : ', url
                #self.logger.info('download this link : ', str(url))
                yield scrapy.Request(url, callback=self.parse_detailed_contents, errback=self.error_back)
            else :
                #print 'follow this link : ', url
                #self.logger.info('follow this link : ', str(url))
                yield scrapy.Request(url, callback=self.parse, errback=self.error_back)
            
            
    #Extract item from the news page
    def parse_detailed_contents(self, response):
        sel = Selector(response)
        #print response.url
        link = response.url
        item = IsentiaTaskItem()
        item['title'] = sel.xpath('//*[@id="article"]/header/div[1]/div/div/h1').extract()
        item['link'] = link
        item['author'] = sel.xpath('//*[@id="article"]/div[2]/div/div[1]/div[2]/p[1]/text()').extract()
        item['content'] = sel.xpath('//*[@id="article"]/div[2]/div/div[1]/div[3]').extract()
        item['published_date'] = sel.xpath('//*[@id="article"]/div[2]/div/div[1]/div[2]/p[2]//text()').extract()
        item['crawled_date'] = ''
        m = re.search(r'http://www.theguardian.com/([\w-]+)/', link)
        if m :
            category = m.group(1)
            item['category'] = category
        else :
            print 'not category link :', link
        print item
        
        
        
    #Self error control
    def error_back(self, response):
        self.logger.error('error in Request')
        