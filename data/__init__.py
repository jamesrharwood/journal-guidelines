from data.preprocess import preprocess
from data.constants import (
    RAW_DATA_FILE_PATH,
    PREPROCESSED_DATA_FILE_PATH,
)


def process():
    preprocess(RAW_DATA_FILE_PATH, PREPROCESSED_DATA_FILE_PATH)


if __name__ == "__main__":
    preprocess()
