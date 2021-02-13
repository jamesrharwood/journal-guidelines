# %%
from .extract import xml_to_csv
from .transform import csv_to_dataframe, save_urls_to_scrape

# %%
if __name__ == "__main__":
    xml_to_csv()
    # %%
    df = csv_to_dataframe()
    df = save_urls_to_scrape(df)
    df.head()


# %%
