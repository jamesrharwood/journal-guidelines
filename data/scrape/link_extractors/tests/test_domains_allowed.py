from .test_link_extractors import Base


class TestDomainsAllowed(Base):
    def test_elsevier_author(self):
        url = "https://www.elsevier.com/authors/policies-and-guidelines/credit-author-statement"
        start = "https://www.elsevier.com"
        self.check_urls_from_url([url], start, target=0)
