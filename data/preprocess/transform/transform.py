# %%
import pandas as pd

from .fields import FIELDS


def transform(IN_FILE_PATH):
    df = pd.read_csv(
        IN_FILE_PATH,
        converters={f.name: f.csv_read_converter for f in FIELDS.extracted},
    )
    for field in FIELDS.preprocessed:
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
