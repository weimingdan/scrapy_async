import asyncio

from scrapy.exceptions import CloseSpider
from scrapy.http import HtmlResponse
from selenium import webdriver
import time
import sys, os

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.webdriver import WebDriver

from scrapy import signals

from selenium.webdriver.chrome.options import Options
from twisted.internet.defer import Deferred


def as_deferred(f):
    """Transform a Twisted Deffered to an Asyncio Future"""

    return Deferred.fromFuture(asyncio.ensure_future(f))


def initDriver():
    option = Options()
    # option.add_argument('--headless')
    option.add_argument('--disable-gpu')
    option.add_argument('--disable-infobars')
    option.add_argument('--disable-extensions')
    option.add_argument("--no-sandbox")
    option.add_argument("--ignore-ssl-errors")
    option.add_argument("--ssl-protocol=TLSv1")
    option.add_argument('--disable-dev-shm-usage')

    driver: WebDriver = webdriver.Chrome(executable_path="D:/Program Files/BitWebV3.0/Chrome/chromedriver.exe", options=option)
    return driver


class CommonMiddleware(object):
    def __init__(self):
        self.driver = initDriver()
        self.main_win = self.driver.current_window_handle  # 记录当前窗口的句柄
        self.all_win = self.driver.window_handles
        self.maxCount = 0

    @classmethod
    def from_crawler(cls, crawler):
        s = cls()
        crawler.signals.connect(s.spider_closed, signal=signals.spider_closed)
        return s

    def spider_closed(self, spider):
        print('close spider')
        self.driver.close()

    async def _process_request(self, request, spider):
        js = f'window.open("");'
        self.driver.execute_script(js)
        # self.all_win = self.driver.current_window_handle
        self.driver.switch_to.window(self.driver.window_handles[-1])
        self.driver.get(request.url)
        content = self.driver.page_source
        return HtmlResponse(self.driver.current_url, body=content, encoding="utf-8")
    def process_request(self, request, spider):
        print(f'load: {request.url}')
        response = as_deferred(self._process_request(request, spider))
        print(f'load finished: {request.url}')
        return response
