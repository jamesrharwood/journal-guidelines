import re

from ..create_extractor import create_extractor
from data.scrape.utils import clean_url

ID = r"[\w-]*/?"
STRATEGIES = []


class Strategy:
    def __init__(self, url_pattern, **extractor_args):
        self.url_pattern = url_pattern
        self.url_regex = re.compile(
            url_pattern.replace(".", r"\."), flags=re.IGNORECASE
        )
        self.extractor_args = extractor_args
        STRATEGIES.append(self)

    def matches_url(self, url):
        url = clean_url(url)
        match = self.url_regex.search(url)
        return bool(match)

    def create_link_extractor(self, url):
        return create_extractor(url, allow_domains=[], **self.extractor_args)

    def __repr__(self):
        return f"<Strategy: {self.url_pattern}>"


sciencedirect = Strategy(
    "www.sciencedirect.com/journal", restrict_text=[r"guide\s*for\s*authors"]
)
elsevier = Strategy(
    f"www.elsevier.com/journals/{ID}",
    restrict_text=[r"guide\s*for\s*authors\s*in\s*pdf"],
)
wiley = Strategy(
    f"onlinelibrary.wiley.com/journal/{ID}$", restrict_text=[r"author\s*guidelines"]
)
springer = Strategy(
    f"www.springer.com/journal/{ID}$", restrict_text=[r"submission\s*guidelines"]
)
tandf = Strategy(
    "www.tandfonline.com/(loi|toc)/", restrict_text=[r"instructions\s*for\s*authors"]
)
sage = Strategy(
    "journals.sagepub.com/home/", restrict_text=[r"submission\s*guidelines"]
)
oup = Strategy(f"academic.oup.com/{ID}$", restrict_text=[r"author\s*guidelines"])
nature = Strategy(f"nature.com/{ID}$", restrict_text=[r"for\s*authors"])
karger = Strategy("karger.com/journal/home/", restrict_text=["guidelines"])
jstage = Strategy(
    f"www.jstage.jst.go.jp/browse/{ID}$", restrict_text=[r"information\s*for\s*authors"]
)
cambridge_home = Strategy(
    f"www.cambridge.org/core/journals/{ID}$",
    restrict_text=["^information"],
)
cambridge_information = Strategy(
    f"www.cambridge.org/core/journals/{ID}/information",
    restrict_text=[r"instructions\s*for\s*authors"],
)
acs = Strategy(f"pubs.acs.org/journal/{ID}", restrict_text=["^authors$"])
jama = Strategy(
    f"jamanetwork.com/journals/{ID}/issue$", restrict_text=[r"for\s*authors"]
)
hindawi = Strategy(f"www.hindawi.com/journals/{ID}$", restrict_text=[r"for\s*authors"])


def get_strategy_for_url(url):
    for strategy in STRATEGIES:
        if strategy.matches_url(url):
            return strategy


def get_extractor_for_url(url):
    strategy = get_strategy_for_url(url)
    extractor = strategy.create_link_extractor(url) if strategy else None
    return extractor
