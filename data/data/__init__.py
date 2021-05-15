import os

DATA_DIR = os.path.dirname(__file__)

RAW_DATA_FILE_PATH = os.path.join(DATA_DIR, "raw.zip")
PREPROCESSED_DATA_FILE_PATH = os.path.join(DATA_DIR, "preprocessed.csv")
SCRAPED_DATA_FILE_PATH = os.path.join(DATA_DIR, "scraped.csv")
POSTPROCESSED_DATA_FILE_PATH = os.path.join(DATA_DIR, "postprocessed.csv")
BROKEN_LINKS_DIR = os.path.join(DATA_DIR, "broken_links")
