import unittest
import os

from scrapy.http import HtmlResponse, Request

from .. import strategies as s
from .targets import TARGETS
from data.scrape.link_extractors.extractors import extract_links

DIR = os.path.dirname(__file__)

URLS = [
    ("https://www.sciencedirect.com/journal/air-medical-journal", s.sciencedirect),
    (
        "https://www.elsevier.com/journals/air-medical-journal/1067-991X/guide-for-authors",
        s.elsevier,
    ),
    ("https://www.springer.com/journal/40257", s.springer),
    ("https://www.tandfonline.com/loi/iaan20", s.tandf),
    ("https://www.tandfonline.com/toc/iaan20/current", s.tandf),
    ("https://journals.sagepub.com/home/ajr", s.sage),
    ("https://academic.oup.com/ajcp", s.oup),
    ("https://academic.oup.com/ajcp/pages/About", None),
    ("https://www.nature.com/srep/", s.nature),
    ("https://www.nature.com/srep/journal-policies", None),
    ("https://www.karger.com/Journal/Home/224270", s.karger),
    ("https://www.jstage.jst.go.jp/browse/ggs/_pubinfo/-char/en", None),
    ("https://www.jstage.jst.go.jp/browse/bio/", s.jstage),
    (
        "https://www.cambridge.org/core/journals/british-journal-for-the-history-of-science",
        s.cambridge_home,
    ),
    (
        (
            "https://www.cambridge.org/core/journals/"
            "british-journal-for-the-history-of-science/information"
        ),
        s.cambridge_information,
    ),
    ("https://onlinelibrary.wiley.com/journal/16121880", s.wiley),
    ("https://pubs.acs.org/journal/aidcbc", s.acs),
    ("https://jamanetwork.com/journals/jamaotolaryngology/issue", s.jama),
    ("https://www.hindawi.com/journals/jitc/", s.hindawi),
]


class TestGetStrategies(unittest.TestCase):
    def test_matches(self):
        for url, strategy in URLS:
            if not strategy:
                continue
            self.assertTrue(
                strategy.matches_url(url),
                f"{url} not a match for {strategy.url_regex.pattern}",
            )

    def test_get(self):
        for url, target in URLS:
            strategy = s.get_strategy_for_url(url)
            self.assertEqual(strategy, target)


class TestStrategyExtractors(unittest.TestCase):
    def test_cambridge_home(self):
        self.check_strategy_regex_matches_text(
            s.cambridge_home,
            "Information about The British Journal for the History of Science",
        )

    def test_cambridge_info(self):
        self.check_strategy_regex_matches_text(
            s.cambridge_information, "\nInstructions for authors\n"
        )

    def check_strategy_regex_matches_text(self, strategy, text):
        extractor = strategy.create_link_extractor("www.test.com")
        regex = extractor.restrict_text[0]
        self.assertTrue(regex.search(text), f"{regex.pattern} does not match {text}")

    def test_extraction_strategies(self):
        for strategy_name in strategy_iterator():
            target = TARGETS[strategy_name]
            response = make_response_for_strategy_name(strategy_name)
            extractor = s.get_extractor_for_url(response.url)
            self.assertTrue(extractor, f"No extractor for URL: {response.url}")
            links = extractor.extract_links(response)
            self.assertTrue(
                len(links),
                (f"{len(links)} links found for strategy: {strategy_name}"),
            )
            self.assertEqual(links[0].url, target)

    def test_extract_links(self):
        for strategy_name in strategy_iterator():
            response = make_response_for_strategy_name(strategy_name)
            links = extract_links(response)
            self.assertEqual(len(links), 1)


def make_response_for_strategy_name(strategy_name):
    file_ = os.path.join(DIR, strategy_name + ".txt")
    url = next((x[0] for x in URLS if x[1] == getattr(s, strategy_name)))
    with open(file_, "r") as infile:
        body = infile.read()
        response = HtmlResponse(
            url=url,
            body=body,
            encoding="utf-8",
            request=Request(url=url, meta={"start_url": url}),
        )
    return response


def strategy_iterator():
    for key in dir(s):
        value = getattr(s, key)
        if isinstance(value, s.Strategy):
            yield key
