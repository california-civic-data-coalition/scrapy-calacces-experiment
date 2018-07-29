import os
import scrapy
from six.moves.urllib.parse import urljoin
from scrapy.selector import Selector


class BaseSpider(scrapy.Spider):
    allowed_domains = ["cal-access.sos.ca.gov",]
    start_urls = []

    def parse_links(self, response):
        # Parse out all hyperlinks with hrefs
        links = response.xpath('*//a/@href').extract()

        # Trim HTML tags down to just the hrefs
        links = [l for l in links if self.link_match in l]

        # Convert them into full URLs
        links = [urljoin("http://cal-access.sos.ca.gov", l) for l in links]

        # Make the list unique
        links = list(set(links))

        # Return it.
        return links

    def write_response(self, response):
        page_name = response.url.split(self.name_split)[-1]
        file_name = '{}-{}.html'.format(self.name, page_name)
        self.write_html(file_name, response)

    def write_html(self, file_name, response):
        self.log('Saving file %s' % file_name)

        # Create the file path
        file_path = os.path.join(self.settings.get("BASE_DIR"), 'html', file_name)

        # Write it out
        with open(file_path, 'w') as f:
            f.write(response.body)
