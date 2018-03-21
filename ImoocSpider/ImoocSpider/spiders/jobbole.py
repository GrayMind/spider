# -*- coding: utf-8 -*-
import scrapy
import re
from urllib import parse
from ImoocSpider.items import JobBoleArticleItem
from ImoocSpider.utils.common import get_md5
from datetime import datetime


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
        # post_urls = response.css('#archive .post.floated-thumb .post-meta a.archive-title::attr(href)').extract()
        post_nodes = response.css('#archive .post.floated-thumb')
        for post_node in post_nodes:
            image_url = post_node.css('.post-thumb a img::attr(src)').extract_first('')
            # if not image_url.startswith('http'):
            #     image_url = parse.urljoin(response.url, image_url)
            post_url = post_node.css('.post-meta a.archive-title::attr(href)').extract_first('')
            yield scrapy.Request(
                url=parse.urljoin(response.url, post_url),
                meta={'front_image_url': parse.urljoin(response.url, image_url)},
                callback=self.parse_detail
            )

        # 解析文章列表中下一页的url，交给scrapy下载
        # next_url = response.css('.next.page-numbers::attr(href)').extract_first('')
        # if next_url:
        #     yield scrapy.Request(url=parse.urljoin(response.url, next_url), callback=self.parse)

    def parse_detail(self, response):
        """
        解析文章详情
        """
        # xpath 方式
        # title = response.xpath('//div[@class="entry-header"]/h1/text()').extract_first('')
        # create_time = response.xpath('//p[@class="entry-meta-hide-on-mobile"]/text()').extract_first('')\
        #     .replace('·', '').strip()
        # praise_num = response.xpath('//span[contains(@class, "vote-post-up")]/h10/text()').extract_first('')
        # fav_num = response.xpath('//span[contains(@class, "bookmark-btn")]/text()').extract_first('')
        # match_re = re.match('.*?(\d+).*', fav_num)
        # if match_re:
        #     fav_num = match_re.group(1)
        # else:
        #     fav_num = '0'
        # comment_num = response.xpath('//a[@href="#article-comment"]/span/text()').extract_first('')
        # match_re = re.match('.*?(\d+).*', comment_num)
        # if match_re:
        #     comment_num = match_re.group(1)
        # else:
        #     comment_num = '0'
        # content = response.xpath('//div[@class="entry"]').extract_first('')
        # tag_list = response.xpath('//p[@class="entry-meta-hide-on-mobile"]/a/text()').extract()
        # tag_list = [e for e in tag_list if not e.strip().endswith('评论')]
        # tags = ','.join(tag_list)


        # css 方式
        # 文章封面图
        front_image_url = response.meta.get('front_image_url', '')
        title = response.css('.entry-header h1::text').extract_first('')
        create_time = response.css('.entry-meta-hide-on-mobile::text').extract_first('').replace('·', '').strip()
        praise_num = response.css('span.vote-post-up h10::text').extract_first('')
        fav_num = response.css('span.bookmark-btn::text').extract_first('')
        match_re = re.match('.*?(\d+).*', fav_num)
        if match_re:
            fav_num = match_re.group(1)
        else:
            fav_num = '0'
        comment_num = response.css('a[href="#article-comment"] span::text').extract_first('')
        match_re = re.match('.*?(\d+).*', comment_num)
        if match_re:
            comment_num = match_re.group(1)
        else:
            comment_num = '0'
        content = response.css('.entry').extract_first('')
        tag_list = response.css('p.entry-meta-hide-on-mobile a::text').extract()
        tag_list = [e for e in tag_list if not e.strip().endswith('评论')]
        tags = ','.join(tag_list)

        article_item = JobBoleArticleItem()
        article_item['title'] = title
        try:
            article_item['create_date'] = datetime.strptime(create_time, '%Y/%m/%d')
        except Exception:
            article_item['create_date'] = None
        article_item['url'] = response.url
        article_item['url_object_id'] = get_md5(response.url)
        article_item['front_image_url'] = [front_image_url]
        # article_item['front_image_path'] = title
        article_item['praise_nums'] = praise_num
        article_item['comment_nums'] = comment_num
        article_item['fav_nums'] = fav_num
        article_item['tags'] = tags
        article_item['content'] = content
        yield article_item
