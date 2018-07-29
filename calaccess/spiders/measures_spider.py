import scrapy
from . import BaseSpider


class MeasuresSpider(BaseSpider):
    name = "measures"
    seed_url = "http://cal-access.sos.ca.gov/Campaign/Measures/list.aspx?session=2015"
    link_match = '?session='
    name_split = "session="
