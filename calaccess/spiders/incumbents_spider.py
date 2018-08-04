# -*- coding: utf-8 -*-
import re
import scrapy
from . import BaseSpider
from bs4 import BeautifulSoup
from datetime import datetime
from calaccess.loaders import IncumbentLoader, IncumbentElectionLoader


class IncumbentsSpider(BaseSpider):
    name = "incumbents"
    start_urls = ["http://cal-access.sos.ca.gov/Campaign/Candidates/list.aspx?view=incumbent&session=2015",]
    link_match = '?view=incumbent&session='
    election_pattern = re.compile(r'^\d+\. (.+)\s+(?:[A-Z][a-z]+day), (\d{1,2}\/\d{1,2}\/\d{2})$')

    def parse(self, response):
        # Parse all the items in the page
        soup = BeautifulSoup(response.body, 'html.parser')
        span_list = soup.find_all('span', class_='txt7')
        for span in span_list:
            match = self.election_pattern.match(span.text)
            if match:
                item = IncumbentElectionLoader()
                item.add_value('session', response.url.split("&session=")[-1])
                item.add_value('name', match.groups()[0].strip())
                item.add_value('date', str(datetime.strptime(match.groups()[1], '%m/%d/%y').date()))
                item.add_value('url', response.url)
                yield item.load_item()

        sections = soup.find_all(
            'table',
            {
                'cellspacing': 0,
                'cellpadding': 4,
                'border': 3,
                'bordercolor': "#3149AA",
                'bgcolor': "#7183C6",
                'width': "100%",
            }
        )
        for section in sections:
            category = section.find('span', class_='hdr14').text.strip()
            for td in section.find_all('td', width="50%"):
                office = td.find('span', class_='txt7').text.strip()
                for a in td.find_all('a', class_='sublink2'):
                    item = IncumbentLoader()
                    item.add_value("id", re.search(r'&id=(\d+)', a['href'].strip()).groups()[0])
                    item.add_value("session", response.url.split("&session=")[-1])
                    item.add_value("category", category)
                    item.add_value("office", office)
                    item.add_value("name", a.text.strip())
                    item.add_value("url", a['href'])
                    yield item.load_item()

        # Recursively request any new links found on this page
        for url in self.parse_links(response):
            yield scrapy.Request(url=url, callback=self.parse)
