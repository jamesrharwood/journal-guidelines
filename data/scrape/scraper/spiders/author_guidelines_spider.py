from dataclasses import dataclass

from scrapy import Request, Spider

from data.constants import JOURNALS_CSV_FILE_PATH
from . import journal_urls
from .link_extractors import create_link_extractor
from ..items import PageDataLoader, PageData


class JournalGuidelinesSpider(Spider):
    name = "journals"
    journal_urls = journal_urls.load_from_csv(JOURNALS_CSV_FILE_PATH)
    journal_urls = [journal_urls[idx] for idx in range(0, len(journal_urls), 256)]

    def start_requests(self):
        requests = [
            Request(journal_url.url, callback=self.parse, meta={"id": journal_url.id})
            for journal_url in self.journal_urls
        ]
        return requests

    def parse(self, response):
        print(response.url)
        page_data_loader = PageDataLoader.create(item=PageData(), response=response)
        page_data_loader.load_item()
        link_extractor = create_link_extractor(response.url)
        for link in link_extractor.extract_links(response):
            yield Request(link.url, callback=self.parse, meta=response.meta)
