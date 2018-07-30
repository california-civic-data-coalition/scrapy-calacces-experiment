# -*- coding: utf-8 -*-
import os
from scrapy import signals
from scrapy.exporters import CsvItemExporter
from scrapy.xlib.pydispatch import dispatcher


class MultiCSVItemPipeline(object):
    item_list = [
        'measureelection',
        'candidateelection',
    ]

    def __init__(self):
        dispatcher.connect(self.spider_opened, signal=signals.spider_opened)
        dispatcher.connect(self.spider_closed, signal=signals.spider_closed)

    def spider_opened(self, spider):
        self.file_dict = {}
        for item in self.item_list:
            file_path = os.path.join(
                spider.settings.get("BASE_DIR"),
                'csv',
                '{}.csv'.format(item)
            )
            self.file_dict[item] = open(file_path, 'wb')

        self.exporters = {}
        for item in self.item_list:
            file = self.file_dict[item]
            self.exporters[item] = CsvItemExporter(file)
        [e.start_exporting() for e in self.exporters.values()]

    def spider_closed(self, spider):
        [e.finish_exporting() for e in self.exporters.values()]
        [f.close() for f in self.file_dict.values()]

    def process_item(self, item, spider):
        what = self.get_item_class(item)
        if what in self.item_list:
            self.exporters[what].export_item(item)
        return item

    def get_item_class(self, item):
        return type(item).__name__.replace('Item', '').lower()
