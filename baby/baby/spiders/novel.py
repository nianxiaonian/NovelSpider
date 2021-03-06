# -*- coding: utf-8 -*-
import copy
import re

import datetime
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class NovelSpider(CrawlSpider):
    name = 'novel'
    allowed_domains = ['mama.cn']
    start_urls = ['http://91baby.mama.cn/']

    rules = (
        # 提取图书列表页，新书热书
        Rule(LinkExtractor(allow=r'http://91baby.mama.cn/forum-200-\d+.html'), follow=True),
        # Rule(LinkExtractor(allow=r'http://91baby.mama.cn/forum-200-\d+.html'), follow=True),
        # 提取图书详情页，经典好文
        Rule(LinkExtractor(restrict_xpaths='//tbody[starts-with(@id,"normalthread")]/tr/th/a[@class="xst"]'), callback='parse_detail', follow=False),
        # Rule(LinkExtractor(allow=r'Items/'), callback='parse_item', follow=True),
    )

    def parse_detail(self, response):
        '''
        提取：name，category，url，author，status，chapter
        :param response:
        :return:
        '''
        item = {}
        # » 《甜》 作者：莫筱薇（书城精品完结）
        # » 《番外在此处》（知否的番外）作者：关心则乱（完结）
        # » 《青蛮》作者:花里(完结)
        title = response.xpath('//div[@class="nav"]/text()[3]').extract_first().replace(' » ', '')
        try:
            if ':' in title:
                if '(' in title:
                    item['name'], item['author'], item['status'] = re.findall(r'(.*?)作者:(.*?)\((.*?)\)$', title)[0]
                elif '（' in title:
                    item['name'], item['author'], item['status'] = re.findall(r'(.*?)作者:(.*?)（(.*?)）$', title)[0]
                else:
                    raise Exception
            elif '：' in title:
                if '(' in title:
                    item['name'], item['author'], item['status'] = re.findall(r'(.*?)作者：(.*?)\((.*?)\)$', title)[0]
                elif '（' in title:
                    item['name'], item['author'], item['status'] = re.findall(r'(.*?)作者：(.*?)（(.*?)）$', title)[0]
                else:
                    raise Exception
            else:
                raise Exception

        except Exception as e:
            print(e)
            item['name'] = title
            item['author'] = None
            item['status'] = None
        if '[91书城]' in item['name']:
            item['name'] = item['name'].replace('[91书城]', '')
        if '【91书城】' in item['name']:
            item['name'] = item['name'].replace('【91书城】', '')
        if '[91书城' in item['name']:
            item['name'] = item['name'].replace('[91书城', '')
        # if '《' in item['name']:
        #     item['name'] = item['name'].replace('《', '')
        # if '《' in item['name']:
        #     item['name'] = item['name'].replace('《', '')
        item['category_name'] = response.xpath('//div[@class="nav"]/a[2]/text()').extract_first()
        item['category_id'] = 1
        item['update_time'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        item['clicks'] = 20
        item['url'] = response.url
        # item['chapter'] = response.xpath('//div[@class="nav"]/a[2]/text()')
        img_ele = response.xpath('//td[@class="t_f"]/img/@src')
        if img_ele:
            item['image'] = img_ele.extract_first()
        else:
            item['image'] = None

        # item['intro'] = ''.join([i.strip() for i in contents[0].xpath('.//text()').extract()])
        # if '\xa0' in item['intro']:
        #     item['intro'] = item['intro'].replace('\xa0', '')
        # item['content'] = ''.join([i.strip() for i in response.xpath('//table//td[@class="t_f"]//text()').extract()])
        item['content'] = ''.join(response.xpath('//table//td[@class="t_f"]').extract())
        if '\xa0' in item['content']:
            item['content'] = item['content'].replace('\xa0', '')

        item['info'] = item['content'].strip()[:100]

        next_ele = response.xpath('//a[@class="nxt"]/@href').extract_first()
        if next_ele:
            yield scrapy.Request(next_ele, callback=self.parse_response_content, meta={'item': copy.deepcopy(item)})
        else:
            yield item

    def parse_response_content(self, response):
        item = response.meta['item']
        item['content'] += ''.join(response.xpath('//table//td[@class="t_f"]').extract())

        next_ele = response.xpath('//a[@class="nxt"]/@href').extract_first()
        if next_ele:
            yield scrapy.Request(next_ele, callback=self.parse_response_content, meta={'item': copy.deepcopy(item)})
        else:
            yield item








