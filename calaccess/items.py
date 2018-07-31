# -*- coding: utf-8 -*-
import scrapy


class CandidateElectionItem(scrapy.Item):
    id = scrapy.Field()
    name = scrapy.Field()
    url = scrapy.Field()


class IncumbentElectionItem(scrapy.Item):
    session = scrapy.Field()
    name = scrapy.Field()
    date = scrapy.Field()
    url = scrapy.Field()


class PropositionElectionItem(scrapy.Item):
    name = scrapy.Field()
    url = scrapy.Field()


class PropositionCommitteeItem(scrapy.Item):
    id = scrapy.Field()
    election_name = scrapy.Field()
    proposition_name = scrapy.Field()
    proposition_id = scrapy.Field()
    name = scrapy.Field()
    position = scrapy.Field()
    url = scrapy.Field()
