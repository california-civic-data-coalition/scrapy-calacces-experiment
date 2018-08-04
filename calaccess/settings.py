# -*- coding: utf-8 -*-
import os
BASE_DIR = os.path.dirname(__file__)

BOT_NAME = 'calaccess'
SPIDER_MODULES = ['calaccess.spiders']
NEWSPIDER_MODULE = 'calaccess.spiders'

ROBOTSTXT_OBEY = False
DOWNLOAD_DELAY = 3
RANDOMIZE_DOWNLOAD_DELAY = True
HTTPCACHE_POLICY = "scrapy.extensions.httpcache.RFC2616Policy"

SPIDER_MIDDLEWARES = {}
DOWNLOADER_MIDDLEWARES = {
    'calaccess.useragent.RotateUserAgentMiddleware' :400,
    'calaccess.middlewares.CalaccessDownloaderMiddleware': 543,
}
ITEM_PIPELINES = {
    'calaccess.pipelines.JsonPipeline': 300,
}
