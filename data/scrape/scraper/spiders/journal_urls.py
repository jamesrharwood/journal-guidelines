import csv
from dataclasses import dataclass

from data.fields import FIELDS


@dataclass
class JournalUrl:
    id: str
    url: str


def load_from_csv(csv_file):
    urls = []
    with open(csv_file) as f:
        for row in csv.DictReader(f, skipinitialspace=True):
            for url in row[FIELDS.urls_filtered_]:
                urls.append(JournalUrl(id=row[FIELDS.id], url=url))
    return urls
