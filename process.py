import sys

from data.preprocess import preprocess as preprocess_
from data.postprocess import postprocess as postprocess_
from data.constants import (
    RAW_DATA_FILE_PATH,
    PREPROCESSED_DATA_FILE_PATH,
    SCRAPED_DATA_FILE_PATH,
    POSTPROCESSED_DATA_FILE_PATH,
)


def preprocess():
    preprocess_(RAW_DATA_FILE_PATH, PREPROCESSED_DATA_FILE_PATH)


def postprocess():
    postprocess_(
        PREPROCESSED_DATA_FILE_PATH,
        SCRAPED_DATA_FILE_PATH,
        POSTPROCESSED_DATA_FILE_PATH,
    )


if __name__ == "__main__":
    globals()[sys.argv[1]]()
