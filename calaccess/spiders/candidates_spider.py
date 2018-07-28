import os
import re
import scrapy
from bs4 import BeautifulSoup
from six.moves.urllib.parse import urljoin


class MeasuresSpider(scrapy.Spider):
    name = "candidates"

    def start_requests(self):
        seed_url = "http://cal-access.sos.ca.gov/Campaign/Candidates/list.aspx?view=certified&electNav=93"
        yield scrapy.Request(url=seed_url, callback=self.parse_seed)

    def parse_seed(self, response):
        self.logger.debug("Parsing seeding URL")
        filename = os.path.join(
            self.settings.get("BASE_DIR"),
            'html',
            'candidates-seed.html'
        )
        with open(filename, 'w') as f:
            f.write(response.body)

        soup = BeautifulSoup(response.body, "html.parser")
        links = soup.findAll('a', href=re.compile(r'^.*\?electNav=\d+'))
        links = [
            l for l in links
            if l.find_next_sibling('span').text != 'Prior Elections'
        ]

        self.logger.debug("{} measure URLs discovered in seed".format(len(links)))
        url_list = list(set([link['href'] for link in links]))

        for url in url_list:
            url = urljoin("http://cal-access.sos.ca.gov", url)
            yield scrapy.Request(url=url, callback=self.save_html)

    def save_html(self, response):
        year = response.url.split("session")[-1]
        filename = os.path.join(
            self.settings.get("BASE_DIR"),
            'html',
            'candidates-{}.html'.format(year)
        )
        with open(filename, 'wb') as f:
            f.write(response.body)
        self.log('Saved file %s' % filename)
