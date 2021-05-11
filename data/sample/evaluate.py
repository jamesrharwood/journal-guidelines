import json
import pandas

from .reference import get_reference_filepath
from .utils import get_filepath_for_sample_and_feed
from data.preprocess.transform.transform import load_csv_to_df
from data.scrape.utils import clean_url as clean_url_params


class Evaluation:
    def __init__(self, sample_name, feed_name=None, feed_path=None):
        self.reference_df = get_reference_df(sample_name)
        self.scraped_df = get_feeds_df(sample_name, feed_name, feed_path)
        self.scraped_df["was_target"] = self.scraped_df["url_cleaned"].apply(
            lambda x: x in self.reference_df["url_cleaned"].to_list()
        )
        self.reference_df["was_scraped"] = self.reference_df.apply(
            url_was_scraped, axis=1, args=(self.scraped_df["url_cleaned"].to_list(),)
        )

    @property
    def sensitivity_counts(self):
        return self.reference_df.was_scraped.value_counts()

    @property
    def urls_scraped_count(self):
        return len(self.scraped_df.index)

    def print_sensitivity(self):
        numerator = self.sensitivity_counts[True]
        denominator = sum(self.sensitivity_counts.values)
        percentage = round(numerator / denominator, 2) * 100
        print(f"Sensitivity: {numerator}/{denominator}, {percentage}%")

    def print_ppv(self):
        numerator = self.sensitivity_counts[True]
        denominator = self.urls_scraped_count
        percentage = round(numerator / denominator, 2) * 100
        print(f"PPV: {numerator}/{denominator}, {percentage}")

    @property
    def urls_scraped(self):
        return self.reference_df[self.reference_df["was_scraped"]].url.tolist()

    @property
    def urls_not_scraped(self):
        return self.reference_df[~self.reference_df["was_scraped"]]

    @property
    def url_tuples_needlessly_scraped(self):
        return [
            (row["url"], row["origin"], row["link_text"])
            for idx, row in self.scraped_df[~self.scraped_df["was_target"]].iterrows()
        ]

    def print_urls_needlessly_scraped(self):
        for url, origin, text in self.url_tuples_needlessly_scraped:
            print(f"{url}\n{origin}\n{text}\n\n")

    def print_urls_not_scraped(self):
        for idx, row in self.urls_not_scraped.iterrows():
            print(f"{row['url']}")

    def summarize(self):
        self.print_sensitivity()
        self.print_ppv()


def get_reference_df(sample_name):
    with open(get_reference_filepath(sample_name), "r") as file_:
        data = json.load(file_)
    df = pandas.DataFrame(data)
    df["url"] = df.apply(combine_url_lists, axis=1)
    df = df.explode("url")
    df = df.dropna(subset=["url"])
    df["url_cleaned"] = df["url"].apply(clean_url)
    return df


def combine_url_lists(row):
    urls = sum(row["urls"].values(), [])
    return urls


def get_feeds_df(sample_name, feed_name=None, feed_path=None):
    path = feed_path or get_filepath_for_sample_and_feed(sample_name, feed_name)
    df = load_csv_to_df(path)
    df = df.dropna(subset=["link_text"])
    df["url_cleaned"] = df["url"].apply(clean_url)
    return df


def url_was_scraped(row, scraped_urls):
    return row["url_cleaned"] in scraped_urls


def clean_url(url):
    url = clean_url_params(url)
    url = url.replace("http://", "")
    url = url.replace("https://", "")
    return url
