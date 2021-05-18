from scrapy.utils.project import get_project_settings
from scrapy.crawler import CrawlerProcess


settings = get_project_settings()


def scrape():
    from data.scrape.spiders import FirstPassSpider, SecondPassSpider, FallbackSpider

    process(FirstPassSpider, SecondPassSpider, FallbackSpider)


def first_scrape():
    from data.scrape.spiders import FirstPassSpider

    process(FirstPassSpider)


def second_scrape():
    from data.scrape.spiders import SecondPassSpider

    process(SecondPassSpider)


def fallback_scrape():
    from data.scrape.spiders import FallbackSpider

    process(FallbackSpider)


def process(*spiders):
    process = CrawlerProcess(settings=settings)
    for spider in spiders:
        process.crawl(spider)
    process.start()
