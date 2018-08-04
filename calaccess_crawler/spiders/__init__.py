import scrapy
from six.moves.urllib.parse import urljoin


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
