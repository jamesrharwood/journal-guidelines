import re

text_list = [
    "service",
    "editor",
    "librar",
    "issue",
    "society",
    "transfer",
    "artwork",
    "media",
    "figure",
    "LaTeX",
    "useful",
    "peer review",
    "video",
    "contributions",
    "declaration",
    r"\?",
    "advertis",
    "reviewer",
    "sample",
    "example",
    r"log\s*in",
    "style",
    "supplement",
    "subscription",
    "privacy",
]
pattern = f'({ "|".join(text_list) })'
regular_expression = re.compile(pattern, flags=re.IGNORECASE)
