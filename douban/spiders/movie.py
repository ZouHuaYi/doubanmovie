# -*- coding: utf-8 -*-

import sys
reload (sys)
sys.setdefaultencoding('utf-8')

import scrapy
from douban.items import DoubanItem 
import json

class MovieSpider(scrapy.Spider):
    name = 'movie'
    allowed_domains = ['movie.douban.com']
    start_urls = u'https://movie.douban.com/j/search_subjects?type=movie&tag=热门&sort=recommend&page_limit=20&page_start=0'
    
    headers = {
        "Accept":r"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8"
        ,"Host":"movie.douban.com"
    	,"Referer":"https://movie.douban.com/explore"
        ,"Cookie":'bid=xBFrO_pyU64; viewed="26274202"; gr_user_id=53c14f3c-3630-425e-87a0-b5b164548a91; _vwo_uuid_v2=2F33C2A2B9203058CBF8736CA8B24F69|b692153a210b98f48c5b58645b623c0d; ll="118281"; __utmc=30149280; __utmz=30149280.1515997536.6.6.utmcsr=baidu|utmccn=(organic)|utmcmd=organic; __utma=30149280.1318808727.1513299286.1516004064.1516007175.8; __utmb=30149280.0.10.1516007175'
    	,"User-Agent":"Mozilla/5.0 (iPhone; CPU iPhone OS 10_3 like Mac OS X) AppleWebKit/602.1.50 (KHTML, like Gecko) CriOS/56.0.2924.75 Mobile/14E5239e Safari/602.1"
    }
    num = 0

    def start_requests(self):
    	yield scrapy.Request(self.start_urls,headers=self.headers,callback=self.parse)

    def parse(self, response):
    	#这是加载json数据的方法
    	data = json.loads(response.body_as_unicode())
    	self.num+=20
    	if len(data["subjects"]):
    		next_url=u'https://movie.douban.com/j/search_subjects?type=movie&tag=热门&sort=recommend&page_limit=20&page_start=%s'%self.num
    		yield data
    		yield scrapy.Request(next_url,callback=self.parse ,headers=self.headers)
    		
    	