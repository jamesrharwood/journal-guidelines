from unittest import TestCase
from scrapy.http import HtmlResponse, Request


from data.scrape import link_extractors as le


URL = "https://www.test.com/"
TEXT = "author guidelines"


class TestLinkExtractorText(TestCase):
    def test_text_matches(self):
        self.check_urls_extracted([TEXT], URL)

    def test_texts_match(self):
        texts = [
            TEXT,
            "Submission guidelines",
            "information",
            "guide",
            "guidelines",
            "guide for authors",
            "guidelines for authors",
            "preparation",
            "how to prepare your manuscript",
            "submission guidelines",
            "submission instructions",
            "manuscript instructions",
            "manuscripts",
            "author checklist",
            "checklist for authors",
            "manuscript checklist",
            "checklist for manuscripts",
            "journal checklist",
            "for authors",
            "instructions for authors",
            "contributors",
            "reporting instructions",
            "reporting",
            "reporting guidelines",
            "article types",
            "article-types",
            "policies",
        ]
        self.check_urls_extracted(texts, URL)

    def test_not_matched(self):
        texts = [
            "service",
            "editors",
            "instructions for editors",
            "editorial information",
            "library",
            "instructions for librarians",
            "issue",
            "issue number",
            "society guidelines",
            "manuscript transfer",
            "manuscript transfers",
            "artwork",
            "guidelines for artwork",
            "media",
            "figures",
            "LaTeX",
            "latex",
            "useful",
            "instructions for peer reviewers",
            "peer review",
            "video",
            "contributions",
        ]
        texts = [TEXT + " " + text for text in texts]
        self.check_urls_extracted(texts, URL, target=0)

    def check_urls_extracted(self, texts, url, target=None, start=None):
        target = len(texts) if target is None else target
        start = url if start is None else start
        html_links = [
            f'<a href="{URL+str(idx)}"">{text}</a>' for idx, text in enumerate(texts)
        ]
        body = f'<body>{"".join(html_links)}</body>'
        request = Request(url, meta={"start_url": start})
        response = HtmlResponse(url, body=body, encoding="utf-8", request=request)
        links = le.extract_links(response)
        if target > 0:
            self.assertTrue(links, response.body)
            for text in texts:
                match = next((link for link in links if link.text == text), None)
                self.assertTrue(match, f"Text not matched: {text}")
        self.assertEqual(
            len(links), target, f"URL: {url}\n\nLINKS: {links}\n\nTEXTS: {texts}"
        )
