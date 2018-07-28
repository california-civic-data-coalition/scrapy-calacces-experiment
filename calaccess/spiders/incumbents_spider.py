import os
import scrapy
from bs4 import BeautifulSoup
from six.moves.urllib.parse import urljoin


class IncumbentsSpider(scrapy.Spider):
    name = "incumbents"
    requested_list = []

    def start_requests(self):
        seed_url = "http://cal-access.sos.ca.gov/Campaign/Candidates/list.aspx?view=incumbent"
        yield scrapy.Request(url=seed_url, callback=self.parse_seed)

    def parse_seed(self, response):
        self.logger.debug("Parsing seeding URL")
        filename = os.path.join(
            self.settings.get("BASE_DIR"),
            'html',
            'incumbents-seed.html'
        )
        with open(filename, 'w') as f:
            f.write(response.body)

        url_list = self.parse_links(response)
        for url in url_list:
            url = urljoin("http://cal-access.sos.ca.gov", url)
            yield scrapy.Request(url=url, callback=self.save_html)

    def parse_links(self, response):
        soup = BeautifulSoup(response.body, "html.parser")
        links = soup.findAll('a', href=True)
        links = [l for l in links if '?view=incumbent&session=' in l['href']]
        links = [l for l in links if l not in self.requested_list]
        self.logger.debug("{} new incumbents URLs discovered".format(len(links)))
        return list(set([link['href'] for link in links]))

    def save_html(self, response):
        self.requested_list.append(response.url)

        year = response.url.split("session=")[-1]
        filename = os.path.join(
            self.settings.get("BASE_DIR"),
            'html',
            'incumbents-{}.html'.format(year)
        )
        with open(filename, 'wb') as f:
            f.write(response.body)
        self.log('Saved file %s' % filename)

        # Request and new links found on this page
        url_list = self.parse_links(response)
        for url in url_list:
            url = urljoin("http://cal-access.sos.ca.gov", url)
            yield scrapy.Request(url=url, callback=self.save_html)
