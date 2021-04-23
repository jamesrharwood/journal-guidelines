from .links_allowed import create_link_matcher_string

text_list = [
    r"\bsearch",
    "crawl",
    "doi",
    "/privacy/",
    "/terms",
    "template",
    "/librar",
    "/solutions",
    "legal",
    "transfer",
    r"peer\W*review",
    "copyright",
    "figure",
    "/full",
    r"log\s*in",
    "reviewer",
    "cookie",
]

string = create_link_matcher_string(text_list)
