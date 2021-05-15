import logging
import os

from scrapy import Request, Spider
from scrapy.http import TextResponse

from data.scrape.utils import get_bytes_from_pdf
from data.data import BROKEN_LINKS_DIR
from .load_urls import (
    load_journal_urls_df_from_csv,
    load_generated_guideline_urls_from_csv,
)
from .link_extractors import extract_links
from .utils import clean_url
from .items import PageDataLoader, PageData
from data.constants import INDEX_COL as IDX, PIVOT_TO_COL as URL


class FallbackSpider(Spider):
    name = "fallback"
    journal_urls_df = load_journal_urls_df_from_csv()

    def start_requests(self):
        requests = [
            Request(
                row[URL],
                callback=self.parse,
                meta={
                    IDX: row[IDX],
                    "visited_urls": [],
                    "link_text": None,
                    "origin": "",
                },
                errback=self.errback,
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

        links = extract_links(response)
        links_to_follow = []
        for link in links:
            cleaned_url = clean_url(link.url)
            if cleaned_url not in response.meta["visited_urls"]:
                response.meta["visited_urls"].append(cleaned_url)
                links_to_follow.append(link)
        response.meta["links_of_interest"] = [
            (link.url, link.text) for link in links_to_follow
        ]

        page_data_loader = PageDataLoader.create(item=PageData(), response=response)
        yield page_data_loader.load_item()

        self.follow_links(links_to_follow, response)

    def follow_links(self, links_to_follow, response):
        for link in links_to_follow:
            meta = {k: v for k, v in response.meta.items()}
            meta.update({"link_text": link.text.strip()})
            meta.update({"origin": response.url})
            yield Request(
                link.url, callback=self.parse, meta=meta, errback=self.errback
            )

    def errback(self, failure):
        response = failure.value.response
        fp = os.path.join(BROKEN_LINKS_DIR, f"{response.status}.txt")
        with open(fp, "a") as file_:
            file_.write("\n" + response.url)


class FirstPassSpider(FallbackSpider):
    name = "first_pass"
    journal_urls_df = load_generated_guideline_urls_from_csv()

    def follow_links(self, *args, **kwargs):
        pass
