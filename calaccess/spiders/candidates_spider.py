import scrapy
from . import BaseSpider


class CandidatesSpider(BaseSpider):
    name = "candidates"
    seed_url = "http://cal-access.sos.ca.gov/Campaign/Candidates/list.aspx?view=certified&electNav=93"
    link_match = "&electNav="
    name_split = "electNav="
