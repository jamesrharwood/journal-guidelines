from data.data import (
    PREPROCESSED_DATA_FILE_PATH as PRE_FP,
    SCRAPED_DATA_FILE_PATH as SCRAPED_FP,
    POSTPROCESSED_DATA_FILE_PATH as POST_FP,
)


from data.postprocess.fields import POSTPROCESSED_FIELDS
from data.preprocess.transform.transform import load_csv_to_df
from data.constants import (
    INDEX_COL,
    PIVOT_TO_COL,
)


def postprocess(
    preprocessed_fp=PRE_FP, scraped_fp=SCRAPED_FP, postprocessed_fp=POST_FP
):
    df = create_pivot_table(preprocessed_fp, scraped_fp)
    df.to_csv(postprocessed_fp)
    return df


def create_pivot_table(PREPROCESSED_DATA_FILE_PATH, SCRAPED_DATA_FILE_PATH):
    journal_df = load_csv_to_df(PREPROCESSED_DATA_FILE_PATH, index_cols=[INDEX_COL])
    scraped_df = load_csv_to_df(
        SCRAPED_DATA_FILE_PATH, index_cols=[INDEX_COL, PIVOT_TO_COL]
    )
    apply_postprocessed_fields(scraped_df)
    df = journal_df.join(scraped_df, how="inner")
    return df


def apply_postprocessed_fields(df):
    for field in POSTPROCESSED_FIELDS:
        field.apply_to_dataframe(df)
