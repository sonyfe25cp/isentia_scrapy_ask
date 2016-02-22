# -*- coding: utf-8 -*-
import scrapy
import re
from scrapy.selector import Selector
from isentia_task.items import IsentiaTaskItem
import time
import html2text


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
        raw_title = sel.xpath('//*[@id="article"]/header/div[1]/div/div/h1/text()').extract()
        item['title'] = combine_text(raw_title)
        item['link'] = link
        raw_author = sel.xpath('//*[@id="article"]/div[2]/div/div[1]/div[2]/p[1]//text()').extract()
        item['author'] = combine_text(raw_author)
        raw_content = sel.xpath('//*[@id="article"]/div[2]/div/div[1]/div[3]//text()').extract()
        item['content'] = combine_text(raw_content)
        raw_published_date = sel.xpath('//*[@id="article"]/div[2]/div/div[1]/div[2]/p[2]//text()').extract()
        item['published_date'] = combine_text(raw_published_date[0:4])
        item['crawled_date'] =  time.strftime('%Y-%m-%d',time.localtime(time.time()))
        m = re.search(r'http://www.theguardian.com/([\w-]+)/', link)
        if m :
            category = m.group(1)
            item['category'] = category
        else :
            print 'not category link :', link
        print item
        return item
    
    
    #Self error control
    def error_back(self, response):
        self.logger.error('error in Request')
        
        
def combine_text(text_list):
    text = ''
    for _text in text_list:
        if _text != '\n':
            text += _text
    return text.replace('\n', '')

#Remove html tags
def clean_html(raw_html):
    html = ''
    if type(raw_html) == 'list':
        for rh in raw_html:
            if rh != '\n':
                html += rh
    else:
        html = raw_html
    text = ''
    if html and len(html) > 0:
        converter = html2text.HTML2Text()
        try:
            text = converter.handle(html)
        except Exception, e:
            text = html
        text = text.replace('\n', '')
            
    return text
        