# import asyncio
# from twisted.internet import asyncioreactor
# asyncioreactor.install(asyncio.get_event_loop())

from scrapy.utils.reactor import install_reactor
install_reactor('twisted.internet.asyncioreactor.AsyncioSelectorReactor')

# Need to install the asyncio reactor before importing Scrapy (?)
# Maybe there is a cleaner way to to it?

from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

import os, sys

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

# import scrapy_async
# import scrapy_async.settings
# import scrapy_async.items
# import scrapy_async.middlewares
# # import scrapy_async.baiduMiddlewares
# import scrapy_async.pipelines
#
# import scrapy.spiderloader
# import scrapy.statscollectors
# import scrapy.logformatter
# import scrapy.dupefilters
# import scrapy.squeues
#
# import scrapy.extensions.spiderstate
# import scrapy.extensions.corestats
# import scrapy.extensions.telnet
# import scrapy.extensions.logstats
# import scrapy.extensions.memusage
# import scrapy.extensions.memdebug
# import scrapy.extensions.feedexport
# import scrapy.extensions.closespider
# import scrapy.extensions.debug
# import scrapy.extensions.httpcache
# import scrapy.extensions.statsmailer
# import scrapy.extensions.throttle
#
# import scrapy.core.scheduler
# import scrapy.core.engine
# import scrapy.core.scraper
# import scrapy.core.spidermw
# import scrapy.core.downloader
#
# import scrapy.downloadermiddlewares.stats
# import scrapy.downloadermiddlewares.httpcache
# import scrapy.downloadermiddlewares.cookies
# import scrapy.downloadermiddlewares.useragent
# import scrapy.downloadermiddlewares.httpproxy
# import scrapy.downloadermiddlewares.ajaxcrawl
# # import scrapy.downloadermiddlewares.chunked
# import scrapy.downloadermiddlewares.decompression
# import scrapy.downloadermiddlewares.defaultheaders
# import scrapy.downloadermiddlewares.downloadtimeout
# import scrapy.downloadermiddlewares.httpauth
# import scrapy.downloadermiddlewares.httpcompression
# import scrapy.downloadermiddlewares.redirect
# import scrapy.downloadermiddlewares.retry
# import scrapy.downloadermiddlewares.robotstxt
#
# import scrapy.spidermiddlewares.depth
# import scrapy.spidermiddlewares.httperror
# import scrapy.spidermiddlewares.offsite
# import scrapy.spidermiddlewares.referer
# import scrapy.spidermiddlewares.urllength
#
# import scrapy.pipelines
#
# import scrapy.core.downloader.handlers.http
# import scrapy.core.downloader.contextfactory

from scrapy_async.spiders.baiduSpider import BaiduSpider
# from toturial.spiders.spider_qqmail import QQMailSpider


# from toturial.spider_setings import baidu_settings
# from toturial.spider_setings import qqmail_settings

from enum import Enum
from enum import IntEnum

class SiteType(IntEnum):
    BAIDU = 1
    QQMAIL = 2

def startCrawler(urls=[]):
    settings = get_project_settings()

    # siteMap = {SiteType.BAIDU: baidu_settings, SiteType.QQMAIL: qqmail_settings}

    site = 1
    # settings.setmodule(siteMap[site])
    # if site == 1:
    #     settings.setmodule(baidu_settings)
    # elif site == 2:
    #     settings.setmodule(qqmail_settings)
    process = CrawlerProcess(settings)
    process.crawl(BaiduSpider)
    process.start()


if __name__ == "__main__":
    startCrawler()