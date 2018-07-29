# -*- coding: utf-8 -*-
import scrapy
from . import BaseSpider


class IncumbentsSpider(BaseSpider):
    name = "incumbents"
    start_urls = ["http://cal-access.sos.ca.gov/Campaign/Candidates/list.aspx?view=incumbent",]
    link_match = '?view=incumbent&session='
    name_split = "session="

    def parse(self, response):
        # Write response
        self.write_response(response)

        # Parse all the items in the page
        pass

        # Recursively request any new links found on this page
        for url in self.parse_links(response):
            yield scrapy.Request(url=url, callback=self.parse)
