import os

from data.constants import PIVOT_FROM_COL, PIVOT_TO_COL, INDEX_COL
from data.data.load import load_csv_to_df, load_scraped
from data.data import PREPROCESSED_DATA_FILE_PATH, SCRAPED_DATA_FILE_PATH
from data.fields import FIELDS


def load_unscraped_urls_df_from_csv(csv_file=PREPROCESSED_DATA_FILE_PATH):
    df = load_journal_urls_df_from_csv(csv_file)
    if not os.path.isfile(SCRAPED_DATA_FILE_PATH):
        return df
    scraped_df = load_scraped()
    df = df.loc[~df[INDEX_COL].isin(scraped_df[INDEX_COL])]
    return df


def load_journal_urls_df_from_csv(csv_file=PREPROCESSED_DATA_FILE_PATH):
    df = load_csv_to_df(csv_file)
    df[PIVOT_TO_COL] = df[PIVOT_FROM_COL].fillna({i: [] for i in df.index})
    df = explode_and_exclude_blanks(df)
    return df


def load_generated_guideline_urls_from_csv(csv_file=PREPROCESSED_DATA_FILE_PATH):
    df = load_csv_to_df(csv_file)
    df[PIVOT_TO_COL] = df[FIELDS.urls_generated_guideline_pages_].fillna(
        {i: [] for i in df.index}
    )
    df = explode_and_exclude_blanks(df)
    return df


def explode_and_exclude_blanks(df, col=PIVOT_TO_COL):
    df = df.explode(PIVOT_TO_COL)
    df = df.dropna(subset=[PIVOT_TO_COL])
    return df
