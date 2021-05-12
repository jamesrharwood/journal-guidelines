from data.fields import FIELDS
from . import (
    PREPROCESSED_DATA_FILE_PATH,
    SCRAPED_DATA_FILE_PATH,
    POSTPROCESSED_DATA_FILE_PATH,
)
from ..constants import INDEX_COL, PIVOT_TO_COL

pd = None


def get_pandas():
    global pd
    if pd is None:
        import pandas

        pd = pandas
    return pd


def load_csv_to_df(in_file_path, index_cols=[]):
    assert FIELDS.id
    pd = get_pandas()
    df = pd.read_csv(
        in_file_path,
        index_col=index_cols,
        converters={f.name: f.deserializer for f in FIELDS},
    )
    return df


def load_preprocessed():
    return load_csv_to_df(PREPROCESSED_DATA_FILE_PATH, [INDEX_COL])


def load_scraped():
    return load_csv_to_df(SCRAPED_DATA_FILE_PATH, [PIVOT_TO_COL])


def load_postprocessed():
    return load_csv_to_df(POSTPROCESSED_DATA_FILE_PATH)
