from scrapy.utils.project import get_project_settings
from scrapy.crawler import CrawlerProcess


settings = get_project_settings()


def first_scrape():
    from data.scrape.spiders import FirstPassSpider

    process(FirstPassSpider)


def scrape():
    from data.scrape.spiders import FallbackSpider

    process(FallbackSpider)


def process(spider):
    process = CrawlerProcess(settings=settings)
    process.crawl(spider)
    process.start()
