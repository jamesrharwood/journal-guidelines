from scrapy.log import ScrapyFileLogObserver
from scrapy.utils.project import get_project_settings
from scrapy.crawler import CrawlerProcess

from data.constants import PREPROCESSED_DATA_FILE_PATH
from data.preprocess.transform.transform import load_csv_to_df
from data.scrape.scraper import JournalSpider
from .generate import now, get_sample_dir_path


settings = get_project_settings()


def scrape(sample_name):
    dirpath = get_sample_dir_path(dirname)
    Spider = make_spider(dirpath, name)


def make_spider(dirpath, name=None):
    name = name or now()
    logpath = get_log_filepath(dirpath, name)

    class SampleSpider(JournalSpider):
        name = "journals_sample_spider"
        journal_urls_df = get_sample_df(dirname)

        def __init__(self, name=None, **kwargs):
            ScrapyFileLogObserver(open(logpath, "w")).start()
            super(JournalSpider, self).__init__(name, **kwargs)

    return SampleSpider


def get_log_filepath(dirpath, **args):
    filename = "_".join(args.insert(0, "log")) + ".txt"
    return os.path.join(dirpath, filename)


def get_sample_df(dirpath):
    df = load_csv_to_df(PREPROCESSED_DATA_FILE_PATH)
    with open(dirpath, "r") as infile:
        sample = json.load(infile)
    idxs = [journal["idx"] for journal in sample]
    df = df.iloc[idxs]
    return df
