# -*- coding: utf-8 -*-
import re
import scrapy
from . import BaseSpider
from bs4 import BeautifulSoup
from calaccess.loaders import CandidateElectionLoader


class CandidatesSpider(BaseSpider):
    name = "candidates"
    start_urls = ["http://cal-access.sos.ca.gov/Campaign/Candidates/list.aspx?view=certified&electNav=62",]
    link_match = "&electNav="
    name_split = "electNav="

    def parse(self, response):
        # Write response
        self.write_response(response)

        # Parse this page's election id
        id = response.url.split(self.name_split)[-1]
        self.logger.debug("Parsing election {}".format(id))

        # Find the link on the page with this id
        soup = BeautifulSoup(response.body, 'lxml')
        links = soup.find_all('a', href=re.compile(r'^.*&electNav=\d+'))
        link = [l for l in links if 'electNav={}'.format(id) in l['href']][-1]

        # Pull the election title from that link
        name = link.find_next_sibling('span').text.strip()

        # Create an item
        item = CandidateElectionLoader(response=response)
        item.add_value('id', id)
        item.add_value('name', name)
        item.add_value('url', response.url)
        yield item.load_item()

        # Recursively request any new links found on this page
        for url in self.parse_links(response):
            yield scrapy.Request(url=url, callback=self.parse)
