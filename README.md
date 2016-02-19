#Crawler task 

Crawl news pages from www.theguardian.com and save data into mongodb.

## How to install ?

`pip install scrapy`

`pip install pymongo`

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
Bloomfilter is used in this project. TODO

## How to get the main content of news?
XPath with Selector is used to extract the specific text we need.


## How to avoid getting banned?
I just list ways to solve this problem, not implemented in this project.
* Collect lots of user agents.
* Use proxies to fetch urls.
    * Tor project.
    * http proxy.
    
## 
