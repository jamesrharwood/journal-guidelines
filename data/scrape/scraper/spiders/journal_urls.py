from random import randint

from data.constants import INDEX_COL, PIVOT_FROM_COL, PIVOT_TO_COL
from data.preprocess.transform.transform import load_csv_to_df


def load_journal_urls_from_csv(csv_file):
    df = load_csv_to_df(csv_file)
    df[PIVOT_TO_COL] = df[PIVOT_FROM_COL].fillna({i: [] for i in df.index})
    df = df.explode(PIVOT_TO_COL)
    df = df.dropna()
    max_ = len(df.index)
    locs = [randint(0, max_) for x in range(100)]
    df = df.iloc[locs]
    df = {'url': 'https://www.karger.com/journal/files/submissionstatementanm-1', 'id':'test'}
    return df
