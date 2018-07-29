# -*- coding: utf-8 -*-
import scrapy


class CandidateElectionItem(scrapy.Item):
    id = scrapy.Field()
    name = scrapy.Field()
    url = scrapy.Field()


class MeasureElectionItem(scrapy.Item):
    name = scrapy.Field()
    url = scrapy.Field()
