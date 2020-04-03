import nest_asyncio
nest_asyncio.apply()
import asyncio
from enum import Enum

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
from arsenic import get_session, keys, browsers, services, stop_session, start_session

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

class PageState(Enum):
    Idle = 1
    Loading = 2
    Finished = 3

class PageInfo(object):
    def __init__(self, page):
        self.page = page
        self.state = PageState.Idle

class CommonMiddleware(object):
    def __init__(self):
        # self.driver = initDriver()
        # self.main_win = self.driver.current_window_handle  # 记录当前窗口的句柄
        # self.all_win = self.driver.window_handles
        self.maxCount = 0
        self.pages = []
        loop = asyncio.get_event_loop()
        # task = asyncio.ensure_future(self.get_browser())
        loop.run_until_complete(self.get_browser())

    async def get_browser(self):
        service = services.Chromedriver(binary="D:/Program Files/BitWebV3.0/Chrome/chromedriver.exe")
        browser = browsers.Chrome()
        for i in range(5):
            session = await start_session(service=service, browser=browser)
            info = PageInfo(session)
            self.pages.append(info)


    @classmethod
    def from_crawler(cls, crawler):
        s = cls()
        crawler.signals.connect(s.spider_closed, signal=signals.spider_closed)
        return s

    async def close_session(self):
        for session in self.pages:
            await stop_session(session.page)

    def spider_closed(self, spider):
        print('close spider')
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.close_session())
    async def get_page(self):
        for page in self.pages:
            if page.state == PageState.Idle:
                page.state = PageState.Loading
                return page
        return None

    async def get_idle_page(self):
        page = None
        while not page:
            page = await self.get_page()
            await asyncio.sleep(0.5)
        return page

    async def switch_tab(self, index):
        handles = await self.session.get_window_handles()
        await self.session.switch_to_window(handles[index])

    async def load_request(self, request):
        # await self.switch_tab(index)
        await self.session.get(request.url)

    async def _process_request(self, request, spider):
        # js = f'window.open("");'
        # self.driver.execute_script(js)
        # # self.all_win = self.driver.current_window_handle
        # self.driver.switch_to.window(self.driver.window_handles[-1])
        # self.driver.get(request.url)
        # content = self.driver.page_source
        page_info = await self.get_idle_page()
        page = page_info.page
        await page.get(request.url)
        content = await page.get_page_source()
        url = await page.get_url()
        page_info.state = PageState.Idle
        return HtmlResponse(url, body=content, encoding="utf-8")
    def process_request(self, request, spider):
        print(f'load: {request.url}')
        response = as_deferred(self._process_request(request, spider))
        print(f'load finished: {request.url}')
        return response
