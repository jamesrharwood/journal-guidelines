url = "www.sciencedirect.com/(science/)?journal/(aip/)?{ID}"
extractor_args = dict(restrict_text=[r"guide\s*for\s*authors"])
template = "https://www.elsevier.com/journals/{ID}/{issn_print}/guide-for-authors"
