# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.item import Item, Field


class weixinItem(Item):
    author = Field()                  # 公众号名称
    gongzhonghao_type = Field()       # 公众号功能
    html = Field()
    weixin_id = Field()

