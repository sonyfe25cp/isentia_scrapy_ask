# Crawler task 

Crawl news pages from www.theguardian.com and save data into mongodb.

## How to install ?

`pip install scrapy`

`pip install pymongo`

`pip install pybloom`

`pip install readability-lxml`

`pip install web.py`

`pip install beautifulsoup4`

`pip install html2text`

## How to run this code?

`scrapy crawl theguardian`

## What's the data structure of news?
The elements I saved in the db are list as follows:

* title
* content
* author
* published_date
* crawled_date
* category
* link


## How to filter duplicate urls?
Bloomfilter is used in this project.

## How to get the main content of news?
XPath with Selector is used to extract the specific text we need.


## How to avoid getting banned?

First, I collect lots of user agents from Google.

Second, many http proxies are used to fetch urls.

Both of them are implemented in middlewares.

    
## Pipeline
A pipeline for mongo is implemented.
`pymongo` is used in this project.


## How to provide an API to check information?
Web.py is used in this project.



## Other things about this task.
If we just want to fetch news articles from now on, `sitemap` is good choice to crawl.
The sitemap provides useful things about news, including images, keywords, title, link, content, author, etc.
But the sitemap only contains the latest 1000 news.
The sitemap of theguardian.com is http://www.theguardian.com/sitemaps/news.xml

If we need to obey the rules of robots, rules in http://www.theguardian.com/robots.txt should be considered.
