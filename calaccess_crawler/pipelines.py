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
    def open_spider(self, spider):
        # Set the export file name based on the spider's name
        self.file_name = "{}.json".format(spider.name)

        # Set the directory where the file will be saved.
        # If the EXPORT_DIR setting has not been configured, save to the save folder as this file.
        self.file_dir = spider.settings.get('EXPORT_DIR', os.path.dirname(__file__))

        # Combine the name and the directory into a full path
        self.file_path = os.path.join(self.file_dir, self.file_name)

        # Open the file
        self.file = open(self.file_path, 'wb')

        # Configure the exporter
        self.exporter = ItemizedJsonLinesItemExporter(self.file, encoding='utf-8', ensure_ascii=False)

        # Start it up.
        self.exporter.start_exporting()

    def close_spider(self, spider):
        self.exporter.finish_exporting()
        # Close the file on the way out.
        self.file.close()

    def process_item(self, item, spider):
        # Nothing too fancy here.
        self.exporter.export_item(item)
        return item
