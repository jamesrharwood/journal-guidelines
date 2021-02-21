from dataclasses import dataclass

from data.constants import INDEX_COL, PIVOT_FROM_COL, PIVOT_TO_COL
from data.preprocess.transform.transform import load_csv_to_df


@dataclass
class JournalUrl:
    id: str
    url: str


def load_journal_urls_from_csv(csv_file):
    df = load_csv_to_df(csv_file)
    df[PIVOT_TO_COL] = df[PIVOT_FROM_COL].fillna({i: [] for i in df.index})
    df = df.explode(PIVOT_TO_COL)
    df = df.reindex(columns=[INDEX_COL, PIVOT_TO_COL])
    df = df.dropna()
    df = df.iloc[:500]
    return df
