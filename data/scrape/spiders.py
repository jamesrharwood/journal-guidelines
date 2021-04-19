import logging

from scrapy import Request, Spider
from scrapy.http import TextResponse

from data.scrape.utils import get_bytes_from_pdf
from data.constants import PREPROCESSED_DATA_FILE_PATH
from .load_urls import load_journal_urls_df_from_csv
from .link_extractors import extract_links, clean_url
from .items import PageDataLoader, PageData
from data.constants import INDEX_COL as IDX, PIVOT_TO_COL as URL


class JournalSpider(Spider):
    name = "journals"
    journal_urls_df = load_journal_urls_df_from_csv(PREPROCESSED_DATA_FILE_PATH)

    def start_requests(self):
        requests = [
            Request(
                row[URL],
                callback=self.parse,
                meta={IDX: row[IDX], "visited_urls": [], "link_text": None},
            )
            for idx, row in self.journal_urls_df.iterrows()
        ]
        logging.info("About to scrape URLS:")
        for r in requests:
            logging.info(r.url)
        return requests

    def parse(self, response):
        print(response.url)
        if not response.meta.get("start_url", None):
            response.meta["start_url"] = response.url

        if not hasattr(response, "text"):
            if response.url.endswith(".pdf"):
                body = get_bytes_from_pdf(response)
            else:
                body = b""
            response = response.replace(body=body, cls=TextResponse)
        page_data_loader = PageDataLoader.create(item=PageData(), response=response)
        yield page_data_loader.load_item()

        links = extract_links(response)
        links = [
            link
            for link in links
            if clean_url(link.url) not in response.meta["vistied_urls"]
        ]
        response.meta["visited_urls"].extend([clean_url(link.url) for link in links])

        for link in links:
            meta = {k: v for k, v in response.meta.items()}
            meta.update({"link_text": link.text.strip()})
            yield Request(link.url, callback=self.parse, meta=meta)
