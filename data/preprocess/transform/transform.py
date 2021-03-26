# %%
import pandas as pd

from .fields import FIELDS as TRANSFORMED_FIELDS
from data.fields import FIELDS

# from data.constants import INDEX_COL


def load_csv_to_df(in_file_path, index_cols=[]):
    assert FIELDS.id
    df = pd.read_csv(
        in_file_path,
        index_col=index_cols,
        converters={f.name: f.deserializer for f in FIELDS},
    )
    return df


def transform(IN_FILE_PATH):
    df = load_csv_to_df(IN_FILE_PATH)
    for field in TRANSFORMED_FIELDS:
        df[field.name] = field.apply_to_dataframe(df)
    df.to_csv(IN_FILE_PATH)


def save_urls_to_scrape(df, filepath):
    url_col = FIELDS.urls_filtered_
    df[url_col] = df[url_col].fillna({i: [] for i in df.index})
    df = df.explode(url_col)
    df = df.set_index(FIELDS.id, url_col)
    df.head()
    df.to_csv(filepath)
    return df
