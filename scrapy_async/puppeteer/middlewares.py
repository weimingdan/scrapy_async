"""This module contains the ``SeleniumMiddleware`` scrapy middleware"""

import asyncio
import logging
from enum import Enum

from pyppeteer import launch
from scrapy import signals
from scrapy.http import HtmlResponse
from twisted.internet.defer import Deferred

from .http import PuppeteerRequest

logging.getLogger('pyppeteer').setLevel(logging.WARNING)
logging.getLogger('websockets.protocol').setLevel(logging.INFO)

def as_deferred(f):
    """Transform a Twisted Deffered to an Asyncio Future"""

    return Deferred.fromFuture(asyncio.ensure_future(f))

class PageState(Enum):
    Idle = 1
    Loading = 2
    Finished = 3

class PageInfo(object):
    def __init__(self, page):
        self.page = page
        self.state = PageState.Idle

class PuppeteerMiddleware:
    """Downloader middleware handling the requests with Puppeteer"""

    def __init__(self):
        self.browser = None
        self.pages = []

    @classmethod
    async def _from_crawler(cls, crawler):
        """Start the browser"""

        middleware = cls()
        middleware.browser = await launch(headless=False,
                                          executablePath="D:/Program Files/BitWebV3.0/Chrome/chrome.exe")
        for i in range(5):
            page = await middleware.browser.newPage()
            await page.setViewport({'width':0, 'height':0})
            info = PageInfo(page)
            middleware.pages.append(info)
        crawler.signals.connect(middleware.spider_closed, signals.spider_closed)

        return middleware

    @classmethod
    def from_crawler(cls, crawler):
        """Initialize the middleware"""

        loop = asyncio.get_event_loop()
        middleware = loop.run_until_complete(
            asyncio.ensure_future(cls._from_crawler(crawler))
        )

        return middleware

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



    async def _process_request(self, request, spider):
        """Handle the request using Puppeteer"""
        pageInfo = await self.get_idle_page()
        page = pageInfo.page
        print(f'load: {request.url}')

        response = await page.goto(request.url, timeout=100000)
        content = await page.content()
        url = page.url
        pageInfo.state = PageState.Idle
        print(f'finished: {request.url}')
        return HtmlResponse(
            url,
            body=str.encode(content),
            encoding='utf-8',
            request=request
        )


        # Cookies
        if isinstance(request.cookies, dict):
            await page.setCookie(*[
                {'name': k, 'value': v}
                for k, v in request.cookies.items()
            ])
        else:
            await page.setCookie(request.cookies)

        # The headers must be set using request interception
        await page.setRequestInterception(True)

        @page.on('request')
        async def _handle_headers(pu_request):
            overrides = {
                'headers': {
                    k.decode(): ','.join(map(lambda v: v.decode(), v))
                    for k, v in request.headers.items()
                }
            }
            await pu_request.continue_(overrides=overrides)

        response = await page.goto(
            request.url
            # {
            #     'waitUntil': request.wait_until
            # },
        )

        if request.wait_for:
            await page.waitFor(request.wait_for)

        if request.screenshot:
            request.meta['screenshot'] = await page.screenshot()

        content = await page.content()
        body = str.encode(content)
        await page.close()

        # Necessary to bypass the compression middleware (?)
        response.headers.pop('content-encoding', None)
        response.headers.pop('Content-Encoding', None)

        return HtmlResponse(
            page.url,
            status=response.status,
            headers=response.headers,
            body=body,
            encoding='utf-8',
            request=request
        )

    def test_asyncdef(self):
        resp = HtmlResponse('http://example.com/index.html', encoding='utf-8', body='qwer')

    async def wait_finished(self):
        await asyncio.sleep(2)

    async def process_request(self, request, spider):
        """Check if the Request should be handled by Puppeteer"""
        print(f'start: {request.url}')
        # await self.wait_finished()
        return self.test_asyncdef()
        # if not isinstance(request, PuppeteerRequest):
        #     return None
        pageInfo = await self.get_idle_page()
        page = pageInfo.page
        print(f'load: {request.url}')

        response = await page.goto(request.url, timeout=100000)
        content = await page.content()
        url = page.url
        pageInfo.state = PageState.Idle
        print(f'finished: {request.url}')
        return HtmlResponse(
            url,
            body=str.encode(content),
            encoding='utf-8',
            request=request
        )

    async def _spider_closed(self):
        await self.browser.close()

    def spider_closed(self):
        """Shutdown the browser when spider is closed"""

        return as_deferred(self._spider_closed())
