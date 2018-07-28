import os
import re
import scrapy


class DummySpider(scrapy.Spider):
    name = "dummy"

    def start_requests(self):
        seed_url = "http://www.example.com/"
        yield scrapy.Request(url=seed_url, callback=self.save_html)

    def save_html(self, response):
        filename = os.path.join(
            self.settings.get("BASE_DIR"),
            'html',
            'dummy.html'
        )
        with open(filename, 'wb') as f:
            f.write(response.body)
        self.log('Saved file %s' % filename)
