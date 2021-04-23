EQUIVALENT_URLS = {
    "www.elsevier.com": "www.sciencedirect.com",
    "link.springer.com": "www.springer.com",
}
REVERSE = {value: key for key, value in EQUIVALENT_URLS.items()}
EQUIVALENT_URLS.update(REVERSE)
