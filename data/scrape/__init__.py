from scrapy.utils.project import get_project_settings
from scrapy.crawler import CrawlerProcess


settings = get_project_settings()


def scrape():
    from data.scrape.spiders import JournalSpider

    process = CrawlerProcess(settings=settings)
    process.crawl(JournalSpider)
    process.start()
