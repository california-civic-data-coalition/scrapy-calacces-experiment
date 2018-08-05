# -*- coding: utf-8 -*-
import os
BASE_DIR = os.path.dirname(__file__)

BOT_NAME = 'calaccess_crawler'
SPIDER_MODULES = ['calaccess_crawler.spiders']
NEWSPIDER_MODULE = 'calaccess_crawler.spiders'

ROBOTSTXT_OBEY = False
DOWNLOAD_DELAY = 3
RANDOMIZE_DOWNLOAD_DELAY = True
HTTPCACHE_POLICY = "scrapy.extensions.httpcache.RFC2616Policy"

SPIDER_MIDDLEWARES = {}
DOWNLOADER_MIDDLEWARES = {
    # 'scrapy.downloadermiddlewares.retry.RetryMiddleware': 90,
    # 'scrapy_proxies.RandomProxy': 100,
    # 'scrapy.downloadermiddlewares.httpproxy.HttpProxyMiddleware': 110,
    # 'calaccess_crawler.middlewares.RotateUserAgentMiddleware': 120,
}
ITEM_PIPELINES = {
    'calaccess_crawler.pipelines.JsonPipeline': 300,
}

EXPORT_DIR = '/tmp/'

# RETRY_TIMES = 10
# RETRY_HTTP_CODES = [500, 503, 504, 400, 403, 404, 408]
# PROXY_MODE = 0
# PROXY_LIST = os.path.join(BASE_DIR, 'proxy_list.txt')
