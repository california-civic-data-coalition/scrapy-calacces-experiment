# -*- coding: utf-8 -*-
import os
BASE_DIR = os.path.dirname(__file__)

BOT_NAME = 'calaccess'
SPIDER_MODULES = ['calaccess.spiders']
NEWSPIDER_MODULE = 'calaccess.spiders'

ROBOTSTXT_OBEY = False
# COOKIES_ENABLED = False
ROTATING_PROXY_LIST_PATH = os.path.join(BASE_DIR, 'proxies.txt')

DOWNLOAD_DELAY = 3
RANDOMIZE_DOWNLOAD_DELAY = True

SPIDER_MIDDLEWARES = {
    'calaccess.middlewares.CalaccessSpiderMiddleware': 543,
}
DOWNLOADER_MIDDLEWARES = {
    # 'rotating_proxies.middlewares.RotatingProxyMiddleware': 610,
    # 'rotating_proxies.middlewares.BanDetectionMiddleware': 620,
    # 'calaccess.useragent.RotateUserAgentMiddleware' :400,
    'calaccess.middlewares.CalaccessDownloaderMiddleware': 543,
}
ITEM_PIPELINES = {
    'calaccess.pipelines.MultiCSVItemPipeline': 300,
}

HTTPCACHE_POLICY = "scrapy.extensions.httpcache.RFC2616Policy"
