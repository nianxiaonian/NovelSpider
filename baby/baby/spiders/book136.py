# -*- coding: utf-8 -*-
import copy
import re

import datetime
import scrapy
import requests

from utils.log import logger


class Book136Spider(scrapy.Spider):
    name = 'book136'
    allowed_domains = ['136book.com']
    start_urls = ['http://www.136book.com/']

    def parse(self, response):
        item = {}
        category_list = response.xpath('//div[@id="top_nav"]/ul/li[position()>1]')
        category_id = 0
        # for category in category_list:
        #     item['clicks'] = 20
        #     item['category_name'] = category.xpath('./a/text()').extract_first()
        #     category_id += 1
        #     item['category_id'] = category_id
        #     category_url = response.urljoin(category.xpath('./a/@href').extract_first())
        #
        #     yield scrapy.Request(category_url, callback=self.parse_list, meta={'item': copy.deepcopy(item)})

        item['clicks'] = 20
        item['category_name'] = category_list[0].xpath('./a/text()').extract_first()
        category_id += 1
        item['category_id'] = category_id
        category_url = response.urljoin(category_list[0].xpath('./a/@href').extract_first())

        yield scrapy.Request(category_url, callback=self.parse_list, meta={'item': copy.deepcopy(item)})

    def parse_list(self, response):
        item = response.meta['item']
        novel_list = response.xpath('//td[@class="main_tdbgall"]/table[position()>2]')
        # for novel in novel_list:
        #     item['image'] = novel.xpath('.//a/img/@src').extract_first()
        #     item['name'] = novel.xpath('.//tr/td[2]/p/strong/a/text()').extract_first()
        #     author = novel.xpath('.//tr/td[2]/p[1]/text()').extract()[1]
        #     # - 作者:暴雪之夜
        #     try:
        #         item['author'] = re.findall(r'(.*)作者:(.*?)$', author, re.S)[0][-1]
        #     except Exception as e:
        #         logger.error(e)
        #         item['author'] = ''
        #
        #     item['url'] = novel.xpath('.//tr/td[2]/p/strong/a/@href').extract_first()
        #     item['info'] = novel.xpath('.//tr/td[2]/p[2]/text()').extract_first()
        #
        #     yield scrapy.Request(item['url'], callback=self.parse_chapter, meta={'item': copy.deepcopy(item)})

        item['image'] = novel_list[0].xpath('.//a/img/@src').extract_first()
        item['name'] = novel_list[0].xpath('.//tr/td[2]/p/strong/a/text()').extract_first()
        author = novel_list[0].xpath('.//tr/td[2]/p[1]/text()').extract()[1]
        # - 作者:暴雪之夜
        try:
            item['author'] = re.findall(r'(.*)作者:(.*?)$', author, re.S)[0][-1]
        except Exception as e:
            logger.error(e)
            item['author'] = ''

        item['url'] = novel_list[0].xpath('.//tr/td[2]/p/strong/a/@href').extract_first()
        item['info'] = novel_list[0].xpath('.//tr/td[2]/p[2]/text()').extract_first()

        yield scrapy.Request(item['url'], callback=self.parse_chapter, meta={'item': copy.deepcopy(item)})


    def parse_chapter(self, response):
        item = response.meta['item']
        if '已完结' in response.text:
            item['status'] = '已完结'
        else:
            item['status'] = ''
        item['update_time'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        # 获取章节列表
        chapter_names = response.xpath('//center/div[2]/ol/li/a/text()').extract()
        chapter_urls = response.xpath('//center/div[2]/ol/li/a/@href').extract()
        # 建立hash表，存储章节url和name的对应信息
        item['chapter_urls_and_names'] = dict(zip(chapter_names,chapter_urls))

        yield item










