from scrapy import Request, Spider

from data.constants import PREPROCESSED_DATA_FILE_PATH
from .journal_urls import load_journal_urls_from_csv
from .link_extractors import create_link_extractor
from ..items import PageDataLoader, PageData
from data.constants import INDEX_COL as IDX, PIVOT_TO_COL as URL


class JournalSpider(Spider):
    name = "journals"
    journal_urls_df = load_journal_urls_from_csv(PREPROCESSED_DATA_FILE_PATH)

    def start_requests(self):
        requests = [
            Request(
                row[URL], callback=self.parse, meta={IDX: row[IDX], "visited_urls": []}
            )
            for idx, row in self.journal_urls_df.iterrows()
        ]
        return requests

    def parse(self, response):
        print(response.url)
        page_data_loader = PageDataLoader.create(item=PageData(), response=response)
        yield page_data_loader.load_item()
        link_extractor = create_link_extractor(response.url)
        for link in link_extractor.extract_links(response):
            if not link.url in response.meta["visited_urls"]:
                response.meta["visited_urls"].append(link.url)
                yield Request(link.url, callback=self.parse, meta=response.meta)
