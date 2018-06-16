# -*- coding: utf-8 -*-
import scrapy
import json
from scrapy import Spider, Request
from wangyiyunSpider.items import CommentItem


class CommentsSpider(scrapy.Spider):
    name = 'comments'
    allowed_domains = ['https://music.163.com']
    start_urls = [
        'http://http://music.163.com/api/v1/resource/comments/R_SO_4_31445772/']

    limit = 20
    offset = 0
    total_pages = 16641
    song_id = 31445772

    comment_url = 'http://music.163.com/api/v1/resource/comments/R_SO_4_' + \
        str(song_id) + '/?limit={limit}&offset={offset}'

    def start_requests(self):
        while(self.offset <= self.total_pages * 20):
            yield Request(self.comment_url.format(limit=self.limit, offset=self.offset), self.parse_comments)
            self.offset += 20

    def parse_comments(self, response):
        results = json.loads(response.text)
        item = CommentItem()
        comments_sum = results.get('comments')
        for comment in comments_sum:
            item['nickname'] = comment['user'].get('nickname')
            item['content'] = comment.get('content')
            item['likedCount'] = comment.get('likedCount')
            yield item
