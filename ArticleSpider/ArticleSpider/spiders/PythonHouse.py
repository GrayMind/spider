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
        # urls = urls[14:15]

        for index, url in enumerate(urls):
            print(url)
            yield scrapy.Request(url, headers=self.headers, callback=self.parse_detail, meta={'index': index})


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
                <body style="font-size: 20px;width: 100%">
                    <h2>{0}</h2>
                    <br/>
                    {1}
                </body>
            </html>
        """.format(title, body)
        body = body.encode('utf-8')
        index = response.meta.get('index')
        filename = 'html/' + str(index) + '.html'

        # match_obj = re.match('.*mid=(\d+).*', response.url)
        # if match_obj:
        #     title = 'html/' + match_obj.group(1) + '.html'

        self.htmls.append(filename)
        with open(filename, 'wb') as f:
            f.write(body)


    def closed(self, reason):
        options = {
            'encoding': "utf-8",
            'page-size': "A4",
            'margin-top': '10mm',
            'margin-right': '8mm',
            'margin-bottom': '10mm',
            'margin-left': '8mm',
        }
        print(self.htmls)
        # self.htmls = sorted(self.htmls)
        config = pdfkit.configuration(wkhtmltopdf=r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe')
        pdfkit.from_file(self.htmls, 'python.pdf', options=options, configuration=config)
        print('------end')

