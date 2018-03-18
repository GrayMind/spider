# -*- coding: utf-8 -*-
import scrapy
from urllib import request
from urllib.error import HTTPError
import time

from scrapy.http.cookies import CookieJar    # 该模块继承自内置的http.cookiejar,操作类似


class MusicSpider(scrapy.Spider):
    name = 'MusicSpider'
    allowed_domains = ['mp.weixin.qq.com']
    start_urls = ['https://mp.weixin.qq.com/s?__biz=MzIxNDA4OTU0NQ==&mid=2651691767&idx=1&sn=0827c5e0ff7d0733a25dcca23adaafd1&chksm=8c55d0d1bb2259c79757ea7ac46cab88e634f8b994fd5dc4d94931bab910dbc218594a9de884&mpshare=1&scene=1&srcid=0204hQRRQQGwbKAUORawtyek#rd']

    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36"
    }
    cookie_jar = CookieJar()

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url, headers=self.headers)

    def parse(self, response):
        qqmusics = response.selector.css('qqmusic')
        self.cookie_jar.extract_cookies(response, response.request)
        errlist = []
        for qqmusic in qqmusics:
            time.sleep(1)
            # audiourl = qqmusic.css('::attr("audiourl")').extract_first().strip()
            music_name = qqmusic.css('::attr("music_name")').extract_first().strip()
            mid = qqmusic.css('::attr("mid")').extract_first().strip()
            audiourl = 'http://isure.stream.qqmusic.qq.com/C200' + mid + '.m4a?guid=1034004351&vkey=77C47E85579F24199BE7FEA7E533FBBB1FCED541CFD6B3D3CADAD375D6EC7BEB401EEED914A1B2E07E95ABA176E2B85A4ECA5B873CF8F538&uin=&fromtag=50&__wxtag__=003a3ccL4BgjgM'
            print(music_name, audiourl)
            try:
                localpath = 'music/' + music_name + '.m4a'
                request.urlretrieve(audiourl, localpath)
            except HTTPError:
                print(HTTPError)
                errlist.append({
                    'audiourl': audiourl,
                    'music_name': music_name
                })

        print(errlist)
