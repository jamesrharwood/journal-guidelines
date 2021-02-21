import os

DATA_DIR = "data/data_files"

RAW_DATA_FILE_PATH = os.path.join(DATA_DIR, "raw.zip")
PREPROCESSED_DATA_FILE_PATH = os.path.join(DATA_DIR, "preprocessed.csv")
SCRAPED_DATA_FILE_PATH = os.path.join(DATA_DIR, "scraped.csv")
POSTPROCESSED_FILE_PATH = os.path.join(DATA_DIR, "postprocessed.csv")


# define the column names for our two index columns
INDEX_COL = "id"
PIVOT_FROM_COL = "urls"
PIVOT_TO_COL = "url"
