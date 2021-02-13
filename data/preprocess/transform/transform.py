# %%
import pandas as pd

from data.constants import JOURNALS_CSV_FILE_PATH as IN_FILE_PATH
from data.fields import FIELDS
import json

from data.regular_expressions import rx


def csv_to_dataframe():
    df = pd.read_csv(
        IN_FILE_PATH,
        converters={f.name: f.csv_read_converter for f in FIELDS.extracted},
    )
    for field in FIELDS.preprocessed:
        df[field.name] = field.apply_to_dataframe(df)
    return df


def save_urls_to_scrape(df):
    url_col = FIELDS.urls_filtered_
    df[url_col] = df[url_col].fillna({i: [] for i in df.index})
    df = df.explode(url_col)
    df = df.set_index(FIELDS.id, url_col)
    df.head()
    df.to_csv(IN_FILE_PATH)
    return df


# %%
def journals_json_to_dataframe():
    with open("data/journals.json", "r") as infile:
        df = pd.DataFrame(json.load(infile))
    return df
