# Crawler task 

Crawl news pages from www.theguardian.com and save data into mongodb.

## How to install ?

`pip install scrapy`, the scrapy engine.

`pip install pymongo`, the driver for mongo db.

`pip install pybloom`, a bloomfilter.

`pip install html2text`, an tool for extracting text from html.

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

Example:

    {
    _id: ObjectId("56c9e15d735804b444e5deb5"),
    category: "world",
    crawled_date: "2016-02-22",
    title: "China to build ventilation 'corridors' in Beijing to help tackle air pollution",
    author: "Reuters in Beijing",
    content: "Authorities in Beijing are reportedly developing a network of ventilation “corridors” to help tackle the city’s notorious air pollution. Related: Beijing issues first pollution red alert as smog engulfs capital  Construction in the zones, which will be created by connecting parks, rivers, lakes, highways and low building blocks, will be strictly controlled and obstacles to air flow will be removed over time, said the Xinhua state news agency, citing Wang Fei, deputy head of Beijing’s urban planning committee, as saying. There will be five large corridors that will be more than 500 metres wide and several smaller ones, the report said, without giving a time frame for the project.Pollution is a sensitive topic in China, spurring public protests every year about environmental degradation, particularly from factories. For Beijing and its surroundings, the government has set a target for 2020 of reducing pollution by 40% from 2013 levels. A senior environment official said on Friday the city’s air quality has improved over the last two years. Beijing frequently features near the top of the list of China’s most polluted cities as emissions from vehicles and heavy industry combine with weather conditions to raise smog levels. The worst bouts of air pollution tend to coincide with periods of low wind. The authorities have increased efforts to reduce air pollution after the city’s first “red alerts” in December last year, when hazardous smog engulfed the city. Beijing will close 2,500 small polluting firms this year as part of efforts to combat pollution, Xinhua reported last month. ",
    link: "http://www.theguardian.com/world/2016/feb/21/china-to-build-ventilation-corridors-in-beijing-to-help-tackle-air-pollution",
    published_date: "Sunday 21 February 2016 05.42 GMT"
    }

## How to filter duplicate urls?
Bloomfilter is used in this project.

## How to get the main content of news?
XPath with Selector is used to extract the specific text we need.
`html2text` is used in this project.

## Where does news pages store?
I stored them in the mongodb at Compose.
Mongo addr: aws-us-east-1-portal.11.dblayer.com:27067

## How to avoid getting banned?

First, I collect lots of user agents from Google.

Second, many http proxies are used to fetch urls. However, free proxies always not stable. If there are enough stable proxies, the performance will be acceptable.

Both of them are implemented in middlewares.

    
## Pipeline
A pipeline for mongo is implemented.
`pymongo` is used in this project.


## How to query keywords from the mongo database?
I implement a client tool to query news with keywords.

`python query.py <key-words>`

Example:

    python query.py China decades
    
Other args:
    
    -h show the help
    -n set the length of results list
    -b set the begin number of results
    
## How to invoke the client from another python program?

    from query import query
    items = query('China', 0, 5)
    for item in items:
        print item['title']

## How to deploy as an public API with an EC2 instance?
An API is implemented based on web.py framework.
The API oupus results in unicode.

Run:
    
    cd api
    PYTHONPATH=.. python server.py

It's easy to deploy this as an public API service.

Example:
    
    http://127.0.0.1:8080/q=Beijing?begin=0&number=15

Args:
    
    q: query words, if there are multiple words, please use comma to seperate.
    begin: the begin number of results
    number: the length of results list

## What about unittest?
unittest is used in thie project.
Because functions in this project are simple and easy to implement, unittest is basic and not cover all functions.

## Other things about this task.
If we just want to fetch news articles from now on, `sitemap` is good choice to crawl.
The sitemap provides useful things about news, including images, keywords, title, link, content, author, etc.
But the sitemap only contains the latest 1000 news.
The sitemap of theguardian.com is http://www.theguardian.com/sitemaps/news.xml

If we need to obey the rules of robots, rules in http://www.theguardian.com/robots.txt should be considered.

