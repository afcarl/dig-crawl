# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

from scrapy.contrib.loader.processor import Join, MapCompose, TakeFirst
from w3lib.html import remove_tags

# def filter_price(value):
#     if value.isdigit():
#         return value

# def lowercase(value):
#     print >> sys.stderr, "Enter lowercase"
#     return str(value).lower()

# def my_remove_tags(value):
#     return "MRT" + remove_tags(value)

# class Product(scrapy.Item):
#     name = scrapy.Field(
#         input_processor=MapCompose(remove_tags),
#         output_processor=Join(),
#     )
#     price = scrapy.Field(
#         input_processor=MapCompose(remove_tags, filter_price),
#         output_processor=TakeFirst(),
#     )


class EroscrawlItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    sitekey = scrapy.Field()
    referer = scrapy.Field()
    sitekey = scrapy.Field()
    original_url = scrapy.Field()
    sid = scrapy.Field()
    download_timestamp = scrapy.Field()
    download_timestamp_utc = scrapy.Field()
    crawl_host = scrapy.Field()

    gender = scrapy.Field()
    hair_color = scrapy.Field()
    height = scrapy.Field()
    weight = scrapy.Field()
    affiliation = scrapy.Field()
    stated_age = scrapy.Field()
    eye_color = scrapy.Field()
    stated_age = scrapy.Field()
    bust = scrapy.Field()
    waist = scrapy.Field()
    hips = scrapy.Field()
    # for VIP, measurements combines bust + waist + hips
    # for now, count on the integrator to fix
    measurements = scrapy.Field()
    ethnicity = scrapy.Field()
    client_restriction = scrapy.Field()
    availability = scrapy.Field()
    location = scrapy.Field()

    phone_number = scrapy.Field()
    email = scrapy.Field()

    image_urls = scrapy.Field()
    images = scrapy.Field()
