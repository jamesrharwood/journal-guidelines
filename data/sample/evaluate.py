import json
import pandas

from .reference import get_reference_filepath
from .scrape import get_filepath_for_sample_and_feed
from data.preprocess.transform.transform import load_csv_to_df
from data.scrape.utils import clean_url


def evaluate(sample_name, feed_name):
    reference_df = get_reference_df(sample_name)
    scraped_df = get_feeds_df(sample_name, feed_name)
    scraped_urls = [clean_url(url) for url in scraped_df["url"]]
    reference_df["was_scraped"] = reference_df.apply(
        url_was_scraped, axis=1, args=(scraped_urls,)
    )
    value_counts = reference_df.was_scraped.value_counts()
    scraped_count = len(scraped_df.index)
    print(value_counts)
    print(f"Sensitivity: {value_counts[True]/sum(value_counts.values)}")
    print(f"{scraped_count} URLs scraped")

    print("\n\nScraped: ")
    for x in reference_df[reference_df["was_scraped"]].url.tolist():
        print(x)
    print("\n\nURLs not scraped: ")
    for x in reference_df[~reference_df["was_scraped"]].url.tolist():
        print(x)


def get_reference_df(sample_name):
    with open(get_reference_filepath(sample_name), "r") as file_:
        data = json.load(file_)
    df = pandas.DataFrame(data)
    df["url"] = df.apply(combine_url_lists, axis=1)
    df = df.explode("url")
    return df


def combine_url_lists(row):
    urls = sum(row["urls"].values(), [])
    urls = [clean_url(url) for url in urls]
    return urls


def get_feeds_df(sample_name, feed_name):
    path = get_filepath_for_sample_and_feed(sample_name, feed_name)
    return load_csv_to_df(path)


def url_was_scraped(row, scraped_urls):
    return row["url"] in scraped_urls
