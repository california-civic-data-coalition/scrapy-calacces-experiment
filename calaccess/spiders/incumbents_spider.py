# -*- coding: utf-8 -*-
import re
import scrapy
from . import BaseSpider
from bs4 import BeautifulSoup
from calaccess.loaders import IncumbentElectionLoader


class IncumbentsSpider(BaseSpider):
    name = "incumbents"
    start_urls = ["http://cal-access.sos.ca.gov/Campaign/Candidates/list.aspx?view=incumbent&session=2015",]
    link_match = '?view=incumbent&session='
    name_split = "session="
    cycle_link_pattern = re.compile(
        r'^/Campaign/Candidates/list\.aspx\?view=incumbent&session=(?P<yr>\d{,4})',
    )

    def parse(self, response):
        # Parse all the items in the page
        soup = BeautifulSoup(response.body, 'lxml')s
        cycle_links = [
            l['href'] for l in soup.find_all(
                'a',
                href=self.cycle_link_pattern,
            )
        ]

        session = self.cycle_link_pattern.search(link).groupdict()['yr']


        # Recursively request any new links found on this page
        for url in self.parse_links(response):
            yield scrapy.Request(url=url, callback=self.parse)
