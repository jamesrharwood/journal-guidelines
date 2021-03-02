#%%
import pandas as pd

from data.postprocess.fields import POSTPROCESSED_FIELDS
from data.preprocess.transform.transform import load_csv_to_df
from data.constants import (
    INDEX_COL,
    PIVOT_TO_COL,
)


def apply_postprocessed_fields(df):
    for field in POSTPROCESSED_FIELDS:
        field.apply_to_dataframe(df)


def create_pivot_table(PREPROCESSED_DATA_FILE_PATH, SCRAPED_DATA_FILE_PATH):
    journal_df = load_csv_to_df(PREPROCESSED_DATA_FILE_PATH, index_cols=[INDEX_COL])
    scraped_df = load_csv_to_df(
        SCRAPED_DATA_FILE_PATH, index_cols=[INDEX_COL, PIVOT_TO_COL]
    )
    apply_postprocessed_fields(scraped_df)
    df = scraped_df.join(journal_df, how="inner")
    return df


def postprocess(PREPROCESSED_FP, SCRAPED_FP, POSTPROCESSED_FP):
    df = create_pivot_table(PREPROCESSED_FP, SCRAPED_FP)
    df.to_csv(POSTPROCESSED_FP)
