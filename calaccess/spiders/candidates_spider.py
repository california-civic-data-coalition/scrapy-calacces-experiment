# -*- coding: utf-8 -*-
import re
import scrapy
from . import BaseSpider
from bs4 import BeautifulSoup
from calaccess.loaders import CandidateLoader, CandidateElectionLoader


class CandidatesSpider(BaseSpider):
    name = "candidates"
    start_urls = ["http://cal-access.sos.ca.gov/Campaign/Candidates/list.aspx?view=certified&electNav=62",]
    link_match = "&electNav="

    def parse(self, response):
        # Parse this page's election id
        election_id = response.url.split("electNav=")[-1]
        self.logger.debug("Parsing election {}".format(id))

        # Find the link on the page with this id
        soup = BeautifulSoup(response.body, 'html.parser')
        links = soup.find_all('a', href=re.compile(r'^.*&electNav=\d+'))
        this_link = [l for l in links if 'electNav={}'.format(election_id) in l['href']][-1]

        # Pull the election title from that link
        name = this_link.find_next_sibling('span').text.strip()

        # Create an item
        item = CandidateElectionLoader(response=response)
        item.add_value('id', election_id)
        item.add_value('name', name)
        item.add_value('url', response.url)
        yield item.load_item()

        # Parse out the candidates
        for section in soup.findAll('a', {'name': re.compile(r'[a-z]+')}):

            # Check that this data matches the structure we expect.
            section_name_el = section.find('span', {'class': 'hdr14'})

            # If it doesn't, skip this one
            if not section_name_el:
                continue

            # Loop through all the rows in the section table
            for office in section.findAll('td'):

                # Check that this data matches the structure we expect.
                title_el = office.find('span', {'class': 'hdr13'})

                # If it doesn't, skip
                if not title_el:
                    continue

                # Pull the candidates out
                candidates = []
                for c in office.findAll('a', {'class': 'sublink2'}):
                    item = CandidateLoader(response=response)
                    item.add_value("office", title_el.text)
                    item.add_value("election_id", election_id)
                    item.add_value("id", re.match(r'.+id=(\d+)', c['href']).group(1))
                    item.add_value("name", c.text)
                    item.add_value("url", response.url)
                    yield item.load_item()

                for c in office.findAll('span', {'class': 'txt7'}):
                    item = CandidateLoader(response=response)
                    item.add_value("office", title_el.text)
                    item.add_value("election_id", election_id)
                    item.add_value("id", "")
                    item.add_value("name", c.text)
                    item.add_value("url", response.url)
                    yield item.load_item()

        # Recursively request any new links found on this page
        for url in self.parse_links(response):
            yield scrapy.Request(url=url, callback=self.parse)
