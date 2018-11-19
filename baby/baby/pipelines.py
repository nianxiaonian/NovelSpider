# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import re

from baby.spiders.novel import NovelSpider
from pymongo import  MongoClient


class BabyPipeline(object):

    def open_spider(self, spider):
        if isinstance(spider, NovelSpider):
            self.client = MongoClient(host='127.0.0.1', port=27017)
            self.collections = self.client['baby']['novel']

    def process_item(self, item, spider):
        if isinstance(spider, NovelSpider):
            self.collections.insert(dict(item))
        return item

    def close_spider(self, spider):
        if isinstance(spider, NovelSpider):
            self.client.close()


class BabyPipelineTxt(object):

    def process_item(self, item, spider):
        if isinstance(spider, NovelSpider):
            f = open('/Users/nianzhidan/Documents/{}.txt'.format(item['name']), 'wb')
            f.write(('作者：{}\n'.format(item['author']).encode('utf-8')))
            f.write(('状态：{}\n'.format(item['status'])).encode('utf-8'))
            f.write(('分类：{}\n'.format(item['category'])).encode('utf-8'))
            f.write(('原文链接地址：{}\n'.format(item['url'])).encode('utf-8'))
            f.write(('封面图片：{}\n'.format(item['image'])).encode('utf-8'))
            f.write('正文\n'.encode('utf-8'))
            for line in re.split(r'。', item['content']):
                if line == "。":
                    f.write(line.encode('utf-8') + '\n'.encode('utf-8'))
                f.write((line + '。' + '\n').encode('utf-8'))
            f.close()
        return item



