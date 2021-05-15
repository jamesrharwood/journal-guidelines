from data.constants import PIVOT_FROM_COL, PIVOT_TO_COL
from data.preprocess.transform.transform import load_csv_to_df
from data.data import PREPROCESSED_DATA_FILE_PATH
from data.fields import FIELDS


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
    df = df.sample(frac=0.1)
    return df


def explode_and_exclude_blanks(df, col=PIVOT_TO_COL):
    df = df.explode(PIVOT_TO_COL)
    df = df.dropna(subset=[PIVOT_TO_COL])
    return df
