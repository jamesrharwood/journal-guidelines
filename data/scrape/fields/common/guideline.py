from ..rx import RX

guideline = RX(
    "guideline",
    pattern=r"(guideline|checklist|standard|statement)s?",
    matches=[
        "guideline",
        "guidelines",
        "statement",
        "statements",
        "standard",
        "standards",
        "checklist",
        "checklists",
    ],
    non_matches=["guides"],
)
