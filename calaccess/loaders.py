# -*- coding: utf-8 -*-
import scrapy
from . import items
from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst


class BaseLoader(ItemLoader):
    """
    Base loader that defaults all fields to a TakeFirst output processer.
    """
    default_output_processor = TakeFirst()


class CandidateLoader(BaseLoader):
    default_item_class = items.CandidateItem


class CandidateElectionLoader(BaseLoader):
    default_item_class = items.CandidateElectionItem


class IncumbentLoader(BaseLoader):
    default_item_class = items.IncumbentItem


class IncumbentElectionLoader(BaseLoader):
    default_item_class = items.IncumbentElectionItem


class PropositionLoader(BaseLoader):
    default_item_class = items.PropositionItem


class PropositionElectionLoader(BaseLoader):
    default_item_class = items.PropositionElectionItem


class PropositionCommitteeLoader(BaseLoader):
    default_item_class = items.PropositionCommitteeItem
