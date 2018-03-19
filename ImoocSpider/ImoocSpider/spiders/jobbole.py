# -*- coding: utf-8 -*-
import scrapy
import re
from urllib import parse


class JobboleSpider(scrapy.Spider):
    name = 'jobbole'
    allowed_domains = ['blog.jobbole.com']
    start_urls = ['http://blog.jobbole.com/all-posts/']

    def parse(self, response):
        """
        1. 获取文章列表页中文章的 url，交给scrapy下载并解析
        2. 获取下一页 url，交给 scrapy 下载，下载完成后交给 parse 解析
        """
        print('页数： ' + response.url)

        # 解析文章列表中所有的url，交给scrapy下载
        post_urls = response.css('#archive .post.floated-thumb .post-meta a.archive-title::attr(href)').extract()
        for post_url in post_urls:
            yield scrapy.Request(url=parse.urljoin(response.url, post_url), callback=self.parse_detail)

        next_url = response.css('.next.page-numbers::attr(href)').extract_first()
        if next_url:
            yield scrapy.Request(url=parse.urljoin(response.url, next_url), callback=self.parse)

    def parse_detail(self, response):
        # xpath
        # title = response.xpath('//div[@class="entry-header"]/h1/text()').extract_first()
        # create_time = response.xpath('//p[@class="entry-meta-hide-on-mobile"]/text()').extract_first()\
        #     .replace('·', '').strip()
        # praise_num = response.xpath('//span[contains(@class, "vote-post-up")]/h10/text()').extract_first()
        # fav_num = response.xpath('//span[contains(@class, "bookmark-btn")]/text()').extract_first()
        # match_re = re.match('.*?(\d+).*', fav_num)
        # if match_re:
        #     fav_num = match_re.group(1)
        # else:
        #     fav_num = '0'
        # comment_num = response.xpath('//a[@href="#article-comment"]/span/text()').extract_first()
        # match_re = re.match('.*?(\d+).*', comment_num)
        # if match_re:
        #     comment_num = match_re.group(1)
        # else:
        #     comment_num = '0'
        # content = response.xpath('//div[@class="entry"]').extract_first()
        # tag_list = response.xpath('//p[@class="entry-meta-hide-on-mobile"]/a/text()').extract()
        # tag_list = [e for e in tag_list if not e.strip().endswith('评论')]
        # tags = ','.join(tag_list)

        # css
        title = response.css('.entry-header h1::text').extract_first()
        create_time = response.css('.entry-meta-hide-on-mobile::text').extract_first().replace('·', '').strip()
        praise_num = response.css('span.vote-post-up h10::text').extract_first()
        fav_num = response.css('span.bookmark-btn::text').extract_first()
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

        print(title + ':' + response.url)
