from calaccess import proxies
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings


proxies.update_proxy_list()

process = CrawlerProcess(get_project_settings())
process.crawl('incumbents')
process.crawl('propositions')
process.crawl('candidates')
process.start()
