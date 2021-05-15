url = r"onlinelibrary.wiley.com/journal/{ID}/(?P<ISSN>\(ISSN\)[\d-]*)"
extractor_args = dict(restrict_text=[r"author\s*guidelines"])
template = (
    "https://onlinelibrary.wiley.com/page/journal/{ID}/{ISSN}/homepage/forauthors.html"
)
