from data.preprocess import preprocess
from data.constants import (
    MEDLINE_XML_ZIP_FILE_PATH,
    JOURNALS_CSV_FILE_PATH,
)

def process():
    preprocess(MEDLINE_XML_ZIP_FILE_PATH, JOURNALS_CSV_FILE_PATH)
