import scrapy
from . import BaseSpider


class IncumbentsSpider(BaseSpider):
    name = "incumbents"
    seed_url = "http://cal-access.sos.ca.gov/Campaign/Candidates/list.aspx?view=incumbent"
    link_match = '?view=incumbent&session='
    name_split = "session="
