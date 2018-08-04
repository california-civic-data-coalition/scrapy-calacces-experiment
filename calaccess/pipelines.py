# -*- coding: utf-8 -*-
import os
from scrapy.utils.python import to_bytes
from scrapy.exporters import JsonLinesItemExporter


class ItemizedJsonLinesItemExporter(JsonLinesItemExporter):
    """
    Override of default JSON exporter.
    """
    def export_item(self, item, **kwargs):
        # Do the typical thing.
        d = dict(super(JsonLinesItemExporter, self)._get_serialized_fields(item, **kwargs))

        # Add the item's class name to the dictionary. This is our customization.
        d['type'] = type(item).__name__.replace('Item', '')

        # Write it out per usual
        data = self.encoder.encode(d) + '\n'
        self.file.write(to_bytes(data, self.encoding))


class JsonPipeline(object):
    """
    Export all the items to a big JSON file.
    """
    def __init__(self):
        self.file_path = os.path.join(os.path.dirname(__file__), 'items.json')
        self.file = open(self.file_path, 'w')
        self.exporter = ItemizedJsonLinesItemExporter(self.file, encoding='utf-8', ensure_ascii=False)
        self.exporter.start_exporting()

    def close_spider(self, spider):
        self.exporter.finish_exporting()
        self.file.close()

    def process_item(self, item, spider):
        self.exporter.export_item(item)
        return item
