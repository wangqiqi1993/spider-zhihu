# -*- coding: utf-8 -*-
import scrapy
import json
import re
from zhihuuser.items import ZhihuuserItem
class ZhihuSpider(scrapy.Spider):
    name = 'zhihu'
    allowed_domains = ['www.zhihu.com']
    start_urls = ['http://www.zhihu.com/']
    start_url='ren-wo-xing-da-jiao-ya'
    user_url = 'https://www.zhihu.com/api/v4/members/{user}?include={include}'
    user_query='allow_message,is_followed,is_following,is_org,is_blocking,employments,answer_count,follower_count,articles_count,gender,badge[?(type=best_answerer)].topics'
    follows_url='https://www.zhihu.com/api/v4/members/{user}/followees?include={include}&offset={offset}&limit={limit}'
    follows_query='data[*].answer_count,articles_count,gender,follower_count,is_followed,is_following,badge[?(type=best_answerer)].topics'
    followers_url='https://www.zhihu.com/api/v4/members/{user}/followers?include={include}&offset={include}&limit={include}'
    followers_query='data[*].answer_count,articles_count,gender,follower_count,is_followed,is_following,badge[?(type=best_answerer)].topics'
    url_token_set=set()
    def start_requests(self):
        yield scrapy.Request(url=self.user_url.format(user=self.start_url,include=self.user_query),callback=self.parse_user)
        yield scrapy.Request(url=self.follows_url.format(user=self.start_url,include=self.follows_query,offset=0,limit=20),callback=self.parse_follows)
        yield scrapy.Request(url=self.followers_url.format(user=self.start_url, include=self.followers_query, offset=0, limit=20),callback=self.parse_followers)
    def parse_user(self, response):
        result=json.loads(response.text)
        item=ZhihuuserItem()
        if result:
            item['answer_count']=result['answer_count']
            item['articles_count']=result['articles_count']
            item['follower_count']=result['follower_count']
            item['gender']=result['gender']
            item['headline']=result['headline']
            item['name']=result['name']
            item['type']=result['type']
            item['url_token']=result['url_token']
            item['user_type']=result['user_type']
            if item['url_token'] not in self.url_token_set:
                yield item
                yield scrapy.Request(url=self.follows_url.format(user=item['url_token'],include=self.follows_query,offset=0,limit=20),callback=self.parse_follows)
                self.url_token_set.add(item['url_token'])
    def parse_follows(self,response):
        results=json.loads(response.text)
        if 'data' in results.keys():
            for result in results['data']:
                url_token=result['url_token']
                yield scrapy.Request(url=self.user_url.format(user=url_token,include=self.user_query),callback=self.parse_user)
        if 'paging' in results.keys() and results['paging']['is_end']==False:
            next_page = results['paging']['next']
            offset=re.findall('https://.*?&offset=(\d+).*?',next_page)[0]
            user_url=re.findall('https://www.zhihu.com/members/(.*?)/followees.*?',next_page)[0]
            print(self.follows_url.format(user=self.user_url,include=self.follows_query,offset=offset,limit=20))
            yield scrapy.Request(url=self.follows_url.format(user=user_url,include=self.follows_query,offset=offset,limit=20),callback=self.parse_follows)#反爬虫
    def parse_followers(self,response):
        results=json.loads(response.text)
        if 'data' in results.keys():
            for result in results['data']:
                url_token=result['url_token']
                yield scrapy.Request(url=self.user_url.format(user=url_token,include=self.user_query),callback=self.parse_user)
        if 'paging' in results.keys() and results['paging']['is_end']==False:
            next_page = results['paging']['next']
            offset=re.findall('https://.*?&offset=(\d+).*?',next_page)[0]
            user_url=re.findall('https://www.zhihu.com/members/(.*?)/followers.*?',next_page)[0]
            print(self.follows_url.format(user=self.user_url,include=self.follows_query,offset=offset,limit=20))
            yield scrapy.Request(url=self.follows_url.format(user=user_url,include=self.follows_query,offset=offset,limit=20),callback=self.parse_follows)#反爬虫








