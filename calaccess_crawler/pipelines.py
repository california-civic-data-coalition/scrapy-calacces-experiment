# -*- coding: utf-8 -*-
import os
import calaccess_crawler
from scrapy.exporters import CsvItemExporter


class ItemCSVPipeline(object):
    """
    Exports each item's records as a separate CSV file.
    """
    file_dict = {}
    exporter_dict = {}

    def __init__(self):
        # Get a list of all the items in this project.
        self.item_list = calaccess_crawler.get_items()

        # Set the directory where the files will be saved.
        # If the SCRAPY_EXPORT_DIR envvar has not been configured
        # save to the save folder as this file.
        self.file_dir = os.environ.get(
            'SCRAPY_EXPORT_DIR',
            os.path.dirname(__file__)
        )

        # Loop through the items and make a JSON file for each one of them.
        for item_klass in self.item_list:
            # Set the export file name based on the item's name
            file_name = "{}.csv".format(item_klass.__name__)

            # Combine the name and the directory into a full path
            file_path = os.path.join(self.file_dir, file_name)

            # Open the file for writing
            file_obj = open(file_path, 'wb')

            # Add it to the file dictionary
            self.file_dict[item_klass.__name__] = file_obj

            # Convert the file into an exporter
            exporter = CsvItemExporter(file_obj)

            # Add it to the file dictionary
            self.exporter_dict[item_klass.__name__] = exporter

        # Start it up.
        [e.start_exporting() for e in self.exporter_dict.values()]

    def spider_closed(self, spider):
        # Close the exporters ...
        [e.finish_exporting() for e in self.exporter_dict.values()]
        # ... and the files.
        [f.close() for f in self.file_dict.values()]

    def process_item(self, item, spider):
        # Look up the exporter for this item type
        item_klass = type(item)
        # Export it
        self.exporter_dict[item_klass.__name__].export_item(item)
        # Pass it through
        return item
