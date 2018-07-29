# -*- coding: utf-8 -*-
import scrapy
from . import BaseSpider
from calaccess.loaders import MeasureElectionLoader


class MeasuresSpider(BaseSpider):
    name = "measures"
    start_urls = ["http://cal-access.sos.ca.gov/Campaign/Measures/list.aspx?session=2015",]
    link_match = '?session='
    name_split = "session="

    def parse(self, response):
        # Write response
        self.write_response(response)

        # Parse all the items in the page
        table_list = response.selector.xpath('*//table[contains(@id, "ListElections1__")]').extract()
        self.logger.debug("{} elections found".format(len(table_list)))

        for table in table_list:
            item = MeasureElectionLoader(response=response)
            selector = Selector(text=table)
            name = selector.xpath('//caption/span/text()').extract_first()
            item.add_value('name', name)
            item.add_value('url', response.url)
            yield item.load_item()

        # Recursively request any new links found on this page
        for url in self.parse_links(response):
            yield scrapy.Request(url=url, callback=self.parse)
