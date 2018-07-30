# -*- coding: utf-8 -*-
import scrapy


class CandidateElectionItem(scrapy.Item):
    id = scrapy.Field()
    name = scrapy.Field()
    url = scrapy.Field()


class IncumbentElectionItem(scrapy.Item):
    session = scrapy.Field()
    date = scrapy.Field()
    url = scrapy.Field()


class PropositionElectionItem(scrapy.Item):
    name = scrapy.Field()
    url = scrapy.Field()
