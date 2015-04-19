import sys
sys.path.append("/usr/local/lib/python2.7/site-packages")

from scrapy import Spider, Item, Field

class Startup(Item):
	name = Field()
	stage = Field()
	value = Field()
	date = Field()

class Category(item):
	name = Field()
	startup = Field()

class Investor(name):
	name = Field()
	startup = Field()	

class CBSpider(Spider):
    name, start_urls = 'crunchbase', ['https://www.crunchbase.com']

    def parse(self, response):
        return [Post(title=e.extract()) for e in response.css("h2 a::text")]
