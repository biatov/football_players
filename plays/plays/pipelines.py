# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from datetime import datetime


class PlaysPipeline(object):
    def open_spider(self, spider):
        self.date = datetime.now().strftime('%Y-%m-%d_%H:%M:%S')
        self.file = open('players_%s.txt' % self.date, 'w')

    def close_spider(self, spider):
        self.file.close()

    def process_item(self, item, spider):
        try:
            for each in item['player_name']:
                line = str(each) + "\n"
                self.file.write(line)
        except KeyError:
            pass
        return item
