# -*- coding: utf-8 -*-
import re
import scrapy
from . import BaseSpider
from bs4 import BeautifulSoup
from scrapy.selector import Selector
from six.moves.urllib.parse import urljoin
from calaccess.loaders import (
    PropositionElectionLoader,
    PropositionCommitteeLoader
)


class PropositionsSpider(BaseSpider):
    name = "propositions"
    start_urls = ["http://cal-access.sos.ca.gov/Campaign/Measures/list.aspx?session=2015",]
    link_match = '?session='

    def parse(self, response):
        # Parse all the items in the page
        table_list = response.selector.xpath('*//table[contains(@id, "ListElections1__")]').extract()
        self.logger.debug("{} elections found".format(len(table_list)))

        # Parse out all the elections
        for table in table_list:
            item = PropositionElectionLoader(response=response)
            selector = Selector(text=table)
            name = selector.xpath('//caption/span/text()').extract_first()
            item.add_value('name', name)
            item.add_value('url', response.url)
            yield item.load_item()

            prop_urls = selector.xpath("//a[@href]/@href").extract()
            for url in prop_urls:
                full_url = urljoin("http://cal-access.sos.ca.gov/Campaign/Measures/", url)
                yield scrapy.Request(
                    url=full_url,
                    callback=self.parse_proposition,
                    meta={
                        "election_name": name,
                    }
                )

        # Recursively request any new links found on this page
        for url in self.parse_links(response):
            yield scrapy.Request(url=url, callback=self.parse)

    def parse_proposition(self, response):
        """
        Scrape all the committees from proposition detail pages.
        """
        soup = BeautifulSoup(response.body, 'lxml')

        proposition_name = soup.find('span', id='measureName').text
        proposition_id = re.match(r'.+id=(\d+)', response.url).group(1)

        # Loop through all the tables on the page
        # which contain the committees on each side of the measure
        for table in soup.findAll('table', cellpadding='4'):
            item = PropositionCommitteeLoader(response=response)
            item.add_value("election_name", response.meta['election_name'])
            item.add_value("proposition_name", proposition_name)
            item.add_value("proposition_id", proposition_id)

            # Pull the data box
            data = table.findAll('span', {'class': 'txt7'})

            # The URL
            committee_url = table.find('a', {'class': 'sublink2'})
            item.add_value("url", urljoin("http://cal-access.sos.ca.gov", committee_url['href']))

            # The name
            committee_name = committee_url.text
            item.add_value("name", committee_name)

            # ID sometimes refers to xref_filer_id rather than filer_id_raw
            committee_id = data[0].text
            item.add_value("id", committee_id)

            # Does the committee support or oppose the measure?
            committee_position = data[1].text.strip()
            item.add_value("position", committee_position)

            # Load it
            yield item.load_item()
