url = r"(link|www).springer.com/journal/{ID}$"
extractor_args = dict(restrict_text=[r"submission\s*guidelines"])
template = "https://www.springer.com/journal/{ID}/submission-guidelines"
