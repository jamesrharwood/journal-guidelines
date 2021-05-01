import re


def join_with_or(strings):
    return "|".join(strings)


text_list = [
    "information",
    "instruction",
    "guide",
    "prepar",
    "submis",
    "manuscript",
    "prepar",
    "author checklist",
    "checklist for authors",
    "checklist for contributors",
    "submission checklist",
    "manuscript checklist",
    "journal checklist",
    "for authors",
    "contributors",
    "requirements",
    "reporting",
    r"article\W+types",
    "polic",
]
patterns = [fr".*{text}.*" for text in text_list]
regular_expressions = [re.compile(pattern, flags=re.IGNORECASE) for pattern in patterns]
