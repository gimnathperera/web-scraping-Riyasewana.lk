# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class RiyasewanaItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    product_name = scrapy.Field()
    product_price = scrapy.Field()
    product_area = scrapy.Field()
    product_detailed_link = scrapy.Field()
    product_contact_number = scrapy.Field()
    product_contact_name = scrapy.Field()
    product_posted_time = scrapy.Field()
    product_source = scrapy.Field()
    pass
