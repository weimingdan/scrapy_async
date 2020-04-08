import asyncio
import time

from scrapy import Request
from scrapy.spiders import Spider

from scrapy_async import data
from scrapy_async.puppeteer.middlewares import PuppeteerRequest
from tenacity import retry
import random

class BaiduSpider(Spider):
    name = 'baidu'

    def __init__(self):
        self.aa = 0
        urls = []
        # for i in range(1, 3):
        #     # https://news.ycombinator.com/news?p=
        #     # https://tieba.baidu.com/p/6161244444?pn=
        #     urls.append(f"https://vmaig.com/article/OllyDbg_use_study_{0 if i<9 else ''}{i+1}.html")
        urls.append('https://www.baidu.com')
        # urls.append('https://www.qq.com')
        data.startTime = time.time()
        self.start_urls = urls

    # def start_requests(self):
    #     data.startTime = time.time()
    #     print(data.startTime)
    #     for url in self.start_urls:
    #         yield PuppeteerRequest(url)

    def close(spider, reason):
        print(f'time used: {time.time() - data.startTime}')

    @retry
    def get_info(self):
        if random.randint(0, 10) > 1:
            raise IOError("Error occurred!!")
        else:
            return "HOHO"


    async def parse(self, response):
        await asyncio.sleep(0.1)
        print(f'parse: {response.url}')
        print(self.get_info())
        return []
        # if 'baidu' in response.url:
        #     return [Request('https://www.sina.com.cn')]
        # yield {'index': 0}
        # print(f'this is qq mail: {response.url[response.url.rindex("=")+1:]}')
