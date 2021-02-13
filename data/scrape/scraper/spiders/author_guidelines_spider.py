import scrapy
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from scrapy.linkextractors import LinkExtractor
from collections import defaultdict
import csv
import re


def process_value(url):
    url = url.lower()
    url = urlparse(url)
    url = url._replace(query=None, fragment=None).geturl()
    return url


def make_match_selector(field, string, flags=[]):
    flags = [f'"{s}"' for s in flags]
    flag_str = ', '.join(flags)
    flag_str = ', '+flag_str if flag_str else flag_str
    return f'//body//*[re:match({field}, "{string}"{flag_str})]'


def make_or_selector(string, flags=['i']):
    link_selector = make_match_selector('@href', string, flags)
    text_selector = make_match_selector('text()', string, flags)
    return f'{link_selector} | {text_selector}'


SELECTORS = {
    'abstract': make_or_selector(r'\babstract\b'),
    'figure': make_or_selector(r'\bfigure'),
    'table': make_or_selector(r'\btable'),
    'consort': make_or_selector(r'\bCONSORT\b'),
    'strobe': make_or_selector(r'\bSTROBE'),
    'prisma': make_or_selector(r'\bPRISMA'),
    'care': make_or_selector(r'[\.\s]CARE', flags=[]),
    'equator': make_or_selector(r'\bequator'),
    'spirit': make_or_selector(r'\bSPIRIT', flags=[]),
    'stard': make_or_selector(r'\bSTARD'),
    'arrive': make_or_selector(r'\bARRIVE', flags=[]),
    'squire': make_or_selector(r'\bSQUIRE'),
}

EQUATOR_LINK = '://www.equator-network.org'

REGEX_STRINGS = {
    'abstract': r'\babstract',
    'figure': r'\bfigures',
    'consort': r'\bconsort\b',
    'strobe': r'\bstrobe',
    'prisma': r'prisma',
    'equator': r'\bequator',
    'spirit': r'\bspirit',
    'arrive': r'\barrive',
    'stard': r'\bstard',
}

REGEXS = {key: re.compile(value, flags=re.IGNORECASE) for key, value in REGEX_STRINGS.items()}
EQAUTOR_LINK_SELECTORS = {
    'http': make_or_selector('http'+EQUATOR_LINK),
    'https': make_or_selector('https'+EQUATOR_LINK)
}

ALLOWED_LINKS = ('information', 'instruction', 'guide', 'prepar',
                 'submi', 'manuscript', 'prepar', 'checklist')
ALLOWED_LINKS = '|'.join(ALLOWED_LINKS)
ALLOWED_LINKS = (r'[^/]/[^\?]*'+f'({ALLOWED_LINKS})')
NOT_ALLOWED_LINKS = ('search', 'crawl',
                     '/doi/', '/privacy/', '/terms/',
                     )


def get_text_from_xml(html):
    # from https://stackoverflow.com/questions/328356/extracting-text-from-html-file-using-python
    soup = BeautifulSoup(html, features="html.parser")

    # kill all script and style elements
    for script in soup(["script", "style"]):
        script.extract()    # rip it out

    # get text
    text = soup.get_text()
    # break into lines and remove leading and trailing space on each
    lines = (line.strip() for line in text.splitlines())
    # break multi-headlines into a line each
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
    # drop blank lines
    text = '\n'.join(chunk for chunk in chunks if chunk)
    return text


def extract_match_from_text(match, text):
    buffer = 50
    start = max(0, match.start() - buffer)
    stop = min(len(text)-1, match.end())
    quote = text[start:stop]
    assert len(quote) < 200
    return text[start:stop]


class QuotesSpider(scrapy.Spider):
    name = "journals"

    with open('medline_journals.csv') as f:
        my_urls = [{'id': row['id'], 'url': row['urls_filtered'],
                    'title': row['title'], 'MESH': row['mesh_headings']}
                   for row in csv.DictReader(f, skipinitialspace=True)]

    def start_requests(self):
        requests = []
        sample = range(0, len(self.my_urls), 8)
        for row_id in sample:
            url_dict = self.my_urls[row_id]
            url = url_dict['url']
            if not url:
                continue
            if not url.startswith('http'):
                url = 'http://'+url
            id = url_dict['id']
            parsed_url = urlparse(url)
            domain = f'{parsed_url.netloc}'
            meta = {'id': id, 'domain': domain, 'start_url': url,
                    'title': url_dict['title'], 'MESH': url_dict['MESH']}
            requests.append(
                scrapy.Request(url, callback=self.parse, meta=meta)
            )
        return requests

    def parse(self, response):
        print(response.url)
        domain = urlparse(response.url).netloc
        link_extractor = LinkExtractor(
            allow=ALLOWED_LINKS,
            deny=NOT_ALLOWED_LINKS,
            allow_domains=domain,
            process_value=process_value,
            unique=True,
        )

        results = defaultdict(list)
        text = get_text_from_xml(response.body.decode('utf-8'))
        for name, pattern in REGEXS.items():
            for match in pattern.finditer(text):
                quote = extract_match_from_text(match, text)
                results[name].append(quote)
        for name, selector in EQAUTOR_LINK_SELECTORS.items():
            if response.xpath(selector):
                results[name].append(name)

        yield {
            'id': response.meta['id'],
            'title': response.meta['title'],
            'MESH': response.meta['MESH'],
            'url': response.url,
            'status': response.status,
            'start_url': response.meta['start_url'],
            'domain': response.meta['domain'],
            'matches': results
        }

        for link in link_extractor.extract_links(response):
            yield scrapy.Request(link.url, callback=self.parse, meta=response.meta)
