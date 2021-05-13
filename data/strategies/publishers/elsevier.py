url = "www.elsevier.com/journals/{ID}"
extractor_args = dict(
    restrict_text=[r"guide\s*for\s*authors\s*in\s*pdf"],
)
template = "https://www.elsevier.com/journals/{ID}/{issn_print}/guide-for-authors"
