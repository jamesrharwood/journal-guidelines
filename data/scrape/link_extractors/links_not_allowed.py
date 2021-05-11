from .links_allowed import create_link_matcher_string

from .domains_not_allowed import DENIED_DOMAINS

text_list = [
    r"\bsearch",
    "crawl",
    "doi",
    "privacy",
    "terms",
    "template",
    "librar",
    "solutions",
    "legal",
    "transfer",
    r"peer\W*review",
    "copyright",
    "figure",
    "full",
    r"log\W*in",
    "reviewer",
    "cookie",
    r"log\W*in",
    r"sign\W*in",
]

string = create_link_matcher_string(text_list)
string = f'({string}|{"|".join(DENIED_DOMAINS)})'
