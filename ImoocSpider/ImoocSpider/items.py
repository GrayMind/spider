# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html
from datetime import datetime
import re
import scrapy
from scrapy.loader import ItemLoader
from scrapy.loader.processors import MapCompose, TakeFirst, Join


class ImoocspiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


def convert_date(value):
    try:
        return datetime.strptime(value, '%Y/%m/%d')
    except Exception:
        return datetime.now().date()


def get_nums(value):
    match_re = re.match('.*?(\d+).*', value)
    if match_re:
        nums = match_re.group(1)
    else:
        nums = '0'
    return int(nums)


def remove_comments_tags(value):
    if '评论' in value:
        return ''
    else:
        return value


def return_value(value):
    return value


class ArticleItemLoader(ItemLoader):
    default_output_processor = TakeFirst()


class JobBoleArticleItem(scrapy.Item):
    title = scrapy.Field()
    create_date = scrapy.Field(
        input_processor=MapCompose(convert_date),
    )
    url = scrapy.Field()
    url_object_id = scrapy.Field()
    # front_image_url 为数组
    front_image_url = scrapy.Field(
        output_processor=MapCompose(return_value)
    )
    front_image_path = scrapy.Field()
    praise_nums = scrapy.Field(
        input_processor=MapCompose(get_nums),
    )
    comment_nums = scrapy.Field(
        input_processor=MapCompose(get_nums),
    )
    fav_nums = scrapy.Field(
        input_processor=MapCompose(get_nums),
    )
    tags = scrapy.Field(
        input_processor=MapCompose(remove_comments_tags),
        output_processor=Join(',')
    )
    content = scrapy.Field()
