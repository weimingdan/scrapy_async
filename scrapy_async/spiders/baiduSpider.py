import time

from scrapy import Request
from scrapy.spiders import Spider

from scrapy_async import data
from scrapy_async.puppeteer.middlewares import PuppeteerRequest


class BaiduSpider(Spider):
    name = 'baidu'

    def __init__(self):
        self.aa = 0
        urls = []
        for i in range(20):
            # https://news.ycombinator.com/news?p=
            # https://tieba.baidu.com/p/6161244444?pn=
            urls.append(f"https://news.ycombinator.com/news?p={i+1}")

        self.start_urls = urls

    def start_requests(self):
        data.startTime = time.time()
        print(data.startTime)
        for url in self.start_urls:
            yield PuppeteerRequest(url)

    def close(spider, reason):
        print(f'time used: {time.time() - data.startTime}')

    def parse(self, response):
        print(f'parse: {response.url}')
        print(f'this is qq mail: {response.url[response.url.rindex("=")+1:]}')
