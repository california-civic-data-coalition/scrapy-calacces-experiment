# -*- coding: utf-8 -*-
import os
import csv
from scrapy import signals
from scrapy.exporters import CsvItemExporter
from scrapy.xlib.pydispatch import dispatcher


class PipelineMixin(object):
    item_list = [
        'candidate',
        'candidateelection',
        'incumbentelection',
        'propositionelection',
        'propositioncommittee',
    ]

    def get_item_class(self, item):
        return type(item).__name__.replace('Item', '').lower()


class MultiCsvItemExporter(CsvItemExporter, PipelineMixin):

    def export_item(self, item):
        if self._headers_not_written:
            self._headers_not_written = False
            self._write_headers_and_set_fields_to_export(item)

        fields = self._get_serialized_fields(
            item,
            default_value='',
            include_empty=True
        )
        values = list(self._build_row(x for _, x in fields))

        # Reopen the CSV for appending to avoid IO error.
        # Total hack.
        file_path = os.path.join(
            os.path.dirname(__file__),
            'csv',
            '{}.csv'.format(self.get_item_class(item))
        )
        self.csv_writer = csv.writer(open(file_path, 'a'))
        self.csv_writer.writerow(values)


class MultiCSVItemPipeline(PipelineMixin):
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
            self.file_dict[item] = open(file_path, 'w+b')

        self.exporters = {}
        for item in self.item_list:
            file = self.file_dict[item]
            self.exporters[item] = MultiCsvItemExporter(file)
        [e.start_exporting() for e in self.exporters.values()]

    def spider_closed(self, spider):
        [e.finish_exporting() for e in self.exporters.values()]
        [f.close() for f in self.file_dict.values()]

    def process_item(self, item, spider):
        what = self.get_item_class(item)
        if what in self.item_list:
            self.exporters[what]
            self.exporters[what].export_item(item)
        return item
