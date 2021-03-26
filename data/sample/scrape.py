import os
import json

from scrapy.utils.project import get_project_settings
from scrapy.crawler import CrawlerProcess

from data.constants import PREPROCESSED_DATA_FILE_PATH
from data.scrape.scraper.spiders.journal_urls import load_journal_urls_from_csv
from data.scrape.scraper.spiders.journals_spider import JournalSpider
from .utils import get_sample_dir_path
from .reference import get_reference_filepath


settings = get_project_settings()
FIELDS = list(settings["FEEDS"].values())[0]["fields"]


def scrape(sample_name):
    Spider = make_spider(sample_name)
    process = CrawlerProcess(settings=settings)
    process.crawl(Spider)
    process.start()


def make_spider(sample_name):
    logpath = get_log_filepath(sample_name)
    sample_data_frame = get_sample_df(sample_name)
    feeds_filepath = get_feeds_filepath(sample_name)

    class SampleSpider(JournalSpider):
        name = "journals_sample_spider"
        journal_urls_df = sample_data_frame
        print(journal_urls_df)
        custom_settings = {
            "FEEDS": {feeds_filepath: {"format": "csv", "fields": FIELDS}},
            "LOG_FILE": logpath,
        }

    return SampleSpider


def get_feeds_filepath(sample_name):
    dirpath = get_sample_dir_path(sample_name)
    return os.path.join(dirpath, "feed_%(time)s.json")


def get_log_filepath(sample_name):
    dirpath = get_sample_dir_path(sample_name)
    return os.path.join(dirpath, "log.txt")


def get_sample_df(sample_name):
    df = load_journal_urls_from_csv(PREPROCESSED_DATA_FILE_PATH)
    print(f"loaded df is {len(df.index)} rows long")
    reference_filepath = get_reference_filepath(sample_name)
    with open(reference_filepath, "r") as infile:
        sample = json.load(infile)
    ids = [journal["id"] for journal in sample]
    print(f"df should have {len(ids)} ids")
    df = df[df["id"].isin(ids)]
    return df
