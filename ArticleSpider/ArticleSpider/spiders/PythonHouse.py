# -*- coding: utf-8 -*-
import scrapy
# from selenium import webdriver
# from ArticleSpider.settings import SELENIUM_WEBDRIVER_PATH
# from scrapy.selector import Selector
import pdfkit
import re
from ArticleSpider.settings import WKHTMLTOPDF_CONFIG_PATH

class PythonhouseSpider(scrapy.Spider):
    name = 'PythonHouse'
    allowed_domains = ['mp.weixin.qq.com']
    start_urls = ['http://mp.weixin.qq.com/s/u9FeqoBaA3Mr0fPCUMbpqA']

    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36"
    }

    htmls = []

    def start_requests(self):
        # brower = webdriver.Chrome(executable_path=SELENIUM_WEBDRIVER_PATH)
        # brower.get('http://mp.weixin.qq.com/s/u9FeqoBaA3Mr0fPCUMbpqA')
        # Selector(text=brower.page_source)
        #
        # brower.quit()

        for url in self.start_urls:
            yield scrapy.Request(url, headers=self.headers)

    def parse(self, response):
        urls = response.selector.css('#js_content p a::attr(href)').extract()
        urls = urls[8:9]
        for url in urls:
            print(url)
            yield scrapy.Request(url, headers=self.headers, callback=self.parse_detail)

    def parse_detail(self, response):
        title = response.selector.css('.rich_media_title::text').extract_first().strip()
        # body = response.selector.css('.rich_media_content ').extract_first()
        p_list = response.selector.css('.rich_media_content p')
        body = ''
        for p in p_list:
            p_text = p.css('span::text').extract_first()
            p_image = p.css('img').extract_first()
            if p_text:
                match_obj = re.match('(^-*.*-$)', p_text)
                if match_obj:
                    print(match_obj.group(1))
                    break
                else:
                    body += p.xpath('.').extract_first()
            if p_image:
                body += p.xpath('.').extract_first()

        body = body.replace('data-src', 'src')
        body = """
                    <html>
                      <head>
                        <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
                        <meta http-equiv="X-UA-Compatible" content="IE=edge">
                        <meta name="viewport" content="width=device-width,initial-scale=1.0,maximum-scale=1.0,user-scalable=0,viewport-fit=cover">
                        <meta name="apple-mobile-web-app-capable" content="yes">
                        <meta name="apple-mobile-web-app-status-bar-style" content="black">
                        <meta name="format-detection" content="telephone=no">
                        <link rel="stylesheet" href="./wechat.css" type="text/css">
                      </head>
                      <body class="zh_CN mm_appmsg rich_media_empty_extra not_in_mm">
                        <div id="js_article" class="rich_media">
                            <div class="rich_media_inner">
                                <div id="page-content" class="rich_media_area_primary">
                                    <div id="img-content">
                                        <h2 class="rich_media_title" id="activity-name">
                                        {0}   
                                        </h2>
                                        {1}
                                    <div>
                                <div>
                            <div>
                        <div>
                      </body>
                      </html>
        """.format(title, body)
        body = body.encode('utf-8')

        title = title + '.html'
        match_obj = re.match('.*mid=(\d+).*', response.url)
        if match_obj:
            title = match_obj.group(1) + '.html'

        self.htmls.append(title)
        with open(title, 'wb') as f:
            f.write(body)

    def closed(self, reason):
        options = {
            'encoding': "utf-8",
            'page-size': "A6",
            'margin-top': '4mm',
            'margin-right': '2mm',
            'margin-bottom': '4mm',
            'margin-left': '2mm',
        }
        print(self.htmls)
        config = pdfkit.configuration(wkhtmltopdf=r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe')
        pdfkit.from_file(self.htmls, 'python.pdf', options=options, configuration=config)
        print('------pdfkit')

