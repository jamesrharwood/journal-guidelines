url = "www.tandfonline.com/(loi|toc)/"
extractor_args = dict(restrict_text=[r"instructions\s*for\s*authors"])
template = "https://www.tandfonline.com/action/authorSubmission?show=instructions&journalCode={ID}"
