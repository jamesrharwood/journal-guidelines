import io
from urllib.parse import urlparse

import pdftotext
from bs4 import BeautifulSoup


def get_text_from_response(response):
    return get_text_from_xml(response.text.encode("utf-8"))


def get_text_from_xml(html):
    # from https://stackoverflow.com/questions/328356/extracting-text-from-html-file-using-python
    soup = BeautifulSoup(html, features="html.parser")

    # kill all script and style elements
    for script in soup(["script", "style"]):
        script.extract()  # rip it out

    # get text
    text = soup.get_text()
    # break into lines and remove leading and trailing space on each
    lines = (line.strip() for line in text.splitlines())
    # break multi-headlines into a line each
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
    # drop blank lines
    text = "\n".join(chunk for chunk in chunks if chunk)
    return text


def get_text_from_pdf(response):
    pdf = pdftotext.PDF(io.BytesIO(response.body))
    text = "\n\n".join(pdf)
    return text


def get_bytes_from_pdf(response):
    text = get_text_from_pdf(response)
    return text.encode()


def extract_match_from_text(match, text):
    buffer = 50
    start = max(0, match.start() - buffer)
    stop = min(len(text) - 1, match.end())
    quote = text[start:stop]
    assert len(quote) < 200
    return text[start:stop]


def clean_url(url):
    url = url.lower()
    url = urlparse(url)
    url = url._replace(query=None, fragment=None).geturl()
    return url
