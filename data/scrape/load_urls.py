from data.constants import PIVOT_FROM_COL, PIVOT_TO_COL
from data.preprocess.transform.transform import load_csv_to_df


def load_journal_urls_df_from_csv(csv_file):
    df = load_csv_to_df(csv_file)
    df[PIVOT_TO_COL] = df[PIVOT_FROM_COL].fillna({i: [] for i in df.index})
    df = df.explode(PIVOT_TO_COL)
    df = df.dropna(subset=[PIVOT_TO_COL])
    return df
