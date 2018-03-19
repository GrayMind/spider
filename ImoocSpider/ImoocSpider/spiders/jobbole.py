# -*- coding: utf-8 -*-
import scrapy
import re


class JobboleSpider(scrapy.Spider):
    name = 'jobbole'
    allowed_domains = ['blog.jobbole.com']
    start_urls = ['http://blog.jobbole.com/112048/']

    def parse(self, response):
        # xpath
        title = response.xpath('//div[@class="entry-header"]/h1/text()').extract_first()
        create_time = response.xpath('//p[@class="entry-meta-hide-on-mobile"]/text()').extract_first()\
            .replace('·', '').strip()
        praise_num = response.xpath('//span[contains(@class, "vote-post-up")]/h10/text()').extract_first()
        fav_num = response.xpath('//span[contains(@class, "bookmark-btn")]/text()').extract_first()
        match_re = re.match('.*?(\d+).*', fav_num)
        if match_re:
            fav_num = match_re.group(1)
        else:
            fav_num = '0'
        comment_num = response.xpath('//a[@href="#article-comment"]/span/text()').extract_first()
        match_re = re.match('.*?(\d+).*', comment_num)
        if match_re:
            comment_num = match_re.group(1)
        else:
            comment_num = '0'
        content = response.xpath('//div[@class="entry"]').extract_first()
        tag_list = response.xpath('//p[@class="entry-meta-hide-on-mobile"]/a/text()').extract()
        tag_list = [e for e in tag_list if not e.strip().endswith('评论')]
        tags = ','.join(tag_list)

        # css
        title = response.css('.entry-header h1::text').extract_first()
        create_time = response.css('.entry-meta-hide-on-mobile::text').extract_first().replace('·', '').strip()
        praise_num = response.css('span.vote-post-up h10::text').extract_first()
        fav_num = response.css('span.bookmark-btn h10::text').extract_first()
        match_re = re.match('.*?(\d+).*', fav_num)
        if match_re:
            fav_num = match_re.group(1)
        else:
            fav_num = '0'
        comment_num = response.css('a[href="#article-comment"] span::text').extract_first()
        match_re = re.match('.*?(\d+).*', comment_num)
        if match_re:
            comment_num = match_re.group(1)
        else:
            comment_num = '0'
        content = response.css('.entry').extract_first()
        tag_list = response.css('p.entry-meta-hide-on-mobile a::text').extract()
        tag_list = [e for e in tag_list if not e.strip().endswith('评论')]
        tags = ','.join(tag_list)
