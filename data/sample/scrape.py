import os
import json

from scrapy.utils.project import get_project_settings
from scrapy.crawler import CrawlerProcess

from data.data import PREPROCESSED_DATA_FILE_PATH
from data.scrape.load_urls import load_journal_urls_df_from_csv
from data.scrape.spiders import FallbackSpider
from .utils import get_sample_dir_path, now, Timer, get_filepath_for_sample_and_feed
from .reference import get_reference_filepath
from .evaluate import Evaluation

settings = get_project_settings()
FIELDS = list(settings["FEEDS"].values())[0]["fields"]


def scrape(sample_name, spider=FallbackSpider):
    Spider = make_spider(sample_name, spider)
    process = CrawlerProcess(settings=settings)
    process.crawl(Spider)
    with Timer():
        process.start()
    evaluation = Evaluation(sample_name, feed_path=Spider.feed_path)
    return evaluation


def make_spider(sample_name, spider):
    logpath = get_log_filepath(sample_name)
    sample_data_frame = get_sample_df(sample_name)
    feed_filepath = get_feeds_filepath(sample_name)

    class SampleSpider(spider):
        name = "journals_sample_spider"
        journal_urls_df = sample_data_frame
        feed_path = feed_filepath
        custom_settings = {
            "FEEDS": {feed_path: {"format": "csv", "fields": FIELDS}},
            "LOG_FILE": logpath,
        }

    return SampleSpider


def get_feeds_filepath(sample_name):
    feed_name = f"{now()}.csv"
    return get_filepath_for_sample_and_feed(sample_name, feed_name)


def get_log_filepath(sample_name):
    dirpath = get_sample_dir_path(sample_name)
    return os.path.join(dirpath, "log.txt")


def get_sample_df(sample_name):
    df = load_journal_urls_df_from_csv(PREPROCESSED_DATA_FILE_PATH)
    reference_filepath = get_reference_filepath(sample_name)
    with open(reference_filepath, "r") as infile:
        sample = json.load(infile)
    ids = [journal["id"] for journal in sample]
    df = df[df["id"].isin(ids)]
    return df
