from unittest import TestCase
from scrapy.http import HtmlResponse, Request


from data.scrape import link_extractors as le


URL = "https://www.test.com"
TEXT = "author guidelines"


class TestLinkExtractorText(TestCase):
    def test_text_matches(self):
        self.check_urls_extracted([TEXT], URL)

    def test_texts_match(self):
        texts = [
            "Submission guidelines",
        ]
        self.check_urls_extracted(texts, URL)

    def check_urls_extracted(self, texts, url, target=None, start=None):
        target = len(texts) if target is None else target
        start = url if start is None else start
        html_links = [f"<a href={URL}>{text}</a>" for text in texts]
        body = f'<body>{"".join(html_links)}</body>'
        request = Request(url, meta={"start_url": start})
        response = HtmlResponse(url, body=body, encoding="utf-8", request=request)
        links = le.extract_links(response)
        self.assertEqual(len(links), target, f"{url}: {texts}")
