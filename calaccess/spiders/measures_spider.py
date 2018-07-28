import os
import re
import scrapy
from bs4 import BeautifulSoup


class MeasuresSpider(scrapy.Spider):
    name = "measures"

    def start_requests(self):
        seed_url = "http://cal-access.sos.ca.gov/Campaign/Measures/list.aspx?session=2015"
        yield scrapy.Request(url=seed_url, callback=self.parse_seed)

    def parse_seed(self, response):
        self.logger.debug("Parsing seeding URL")
        filename = os.path.join(
            self.settings.get("BASE_DIR"),
            'html',
            'measures-seed.html'
        )
        with open(filename, 'w') as f:
            f.write(response.body)

        soup = BeautifulSoup(response.body, "html.parser")
        links = soup.findAll('a', href=re.compile(r'^.*\?session=\d+'))

        self.logger.debug("{} measure URLs discovered in seed".format(len(links)))
        url_list = list(set([link['href'] for link in links]))

        for url in url_list:
            yield scrapy.Request(url=url, callback=self.save_html)

    def save_html(self, response):
        year = response.url.split("session")[-1]
        filename = os.path.join(
            self.settings.get("BASE_DIR"),
            'html',
            'measures-{}.html'.format(year)
        )
        with open(filename, 'wb') as f:
            f.write(response.body)
        self.log('Saved file %s' % filename)
