import sys

from .preprocess import preprocess as preprocess_
from .scrape import scrape as scrape_
from .postprocess import postprocess as postprocess_
from .data import (
    RAW_DATA_FILE_PATH,
    PREPROCESSED_DATA_FILE_PATH,
    SCRAPED_DATA_FILE_PATH,
    POSTPROCESSED_DATA_FILE_PATH,
)


def preprocess():
    preprocess_(RAW_DATA_FILE_PATH, PREPROCESSED_DATA_FILE_PATH)


def scrape():
    scrape_()


def postprocess():
    postprocess_(
        PREPROCESSED_DATA_FILE_PATH,
        SCRAPED_DATA_FILE_PATH,
        POSTPROCESSED_DATA_FILE_PATH,
    )
