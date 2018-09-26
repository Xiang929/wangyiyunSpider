# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html

import json
import logging
from scrapy import signals
import requests
import random


class ProxyMiddleware():
    def __init__(self, proxy_url):
        self.logger = logging.getLogger(__name__)
        self.proxy_url = proxy_url
        self.proxy = ''

    def get_random_proxy(self):
        try:
            response = requests.get(self.proxy_url)
            if response.status_code == 200:
                proxy = response.text
                return proxy
        except requests.ConnectionError:
            return False

    def process_request(self, request, spider):
        # if request.meta.get('retry_times'):
        if len(self.proxy):
            uri = 'http://{proxy}'.format(proxy=self.proxy)
            self.logger.debug('proxy: ' + self.proxy)
            request.meta['proxy'] = uri
            self.proxy = ''
            

    def process_response(self, request, response, spider):
        if 'Cheating' in response.text:
            self.proxy = self.get_random_proxy()
            return request
        return response

    @classmethod
    def from_crawler(cls, crawler):
        settings = crawler.settings
        return cls(
            proxy_url=settings.get('PROXY_URL')
        )

class RandomUserAgentMiddleware():
	def __init__(self, agents):
		self.agents = agents

	@classmethod
	def from_crawler(cls, crawler):
		return cls(crawler.settings.getlist('USER_AGENTS'))

	def process_request(self, request, spider):
		request.headers.setdefault('User-Agent', random.choice(self.agents))
