# -*- coding: utf-8 -*-
import scrapy
from . import items
from scrapy.loader import ItemLoader


class CandidateElectionLoader(ItemLoader):
    default_item_class = items.CandidateElectionItem


class IncumbentElectionLoader(ItemLoader):
    default_item_class = items.IncumbentElectionItem


class PropositionElectionLoader(ItemLoader):
    default_item_class = items.PropositionElectionItem
