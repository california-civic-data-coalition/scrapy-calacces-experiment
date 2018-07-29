import os
import scrapy
from bs4 import BeautifulSoup
from six.moves.urllib.parse import urljoin


class BaseSpider(scrapy.Spider):
    requested_urls = []

    def start_requests(self):
        yield scrapy.Request(url=self.seed_url, callback=self.parse_seed)

    def parse_seed(self, response):
        # Log what we're doing
        self.logger.debug("Parsing seeding URL")

        # Add URL to global list of what's been harvested
        self.requested_urls.append(self.seed_url)

        # Write out the file
        self.write_html('{}-seed.html'.format(self.name), response)

        # Download all of the pages linked from the seed
        for url in self.parse_links(response):
            yield scrapy.Request(url=url, callback=self.handle_response)

    def parse_links(self, response):
        soup = BeautifulSoup(response.body, "html.parser")

        # Parse out all hyperlinks with hrefs
        links = soup.findAll('a', href=True)

        # Trim HTML tags down to just the hrefs
        links = [l['href'] for l in links if self.link_match in l['href']]

        # Convert them into full URLs
        links = [urljoin("http://cal-access.sos.ca.gov", l) for l in links]

        # Dump any we have already requested
        links = [l for l in links if l not in self.requested_urls]

        # Make the list unique
        links = list(set(links))

        # Log what's left
        self.logger.debug("{} URLs discovered".format(len(links)))

        # Return it.
        return links

    def handle_response(self, response):
        # Add to our global list of scraped pages
        self.requested_urls.append(response.url)

        # Write out the file
        page_name = response.url.split(self.name_split)[-1]
        file_name = '{}-{}.html'.format(self.name, page_name)
        self.write_html(file_name, response)

        # Recursively request any new links found on this page
        for url in self.parse_links(response):
            yield scrapy.Request(url=url, callback=self.handle_response)

    def write_html(self, file_name, response):
        # Log what we're doing
        self.log('Saving file %s' % file_name)

        # Create the file path
        file_path = os.path.join(self.settings.get("BASE_DIR"), 'html', file_name)

        # Write it out
        with open(file_path, 'w') as f:
            f.write(response.body)
