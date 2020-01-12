from dataclasses import dataclass, field
from typing import List

import requests
from lxml import html
import sys
import traceback


class Downloader:
    @staticmethod
    def get(url):
        try:
            r = requests.get(url)
            if r.status_code != 200:
                raise Exception(f'Request ended with status code: '
                                f'{r.status_code}')
            return r.text
        except Exception as e:
            raise RuntimeError("Could not connect to host") from e


@dataclass
class TorrentRow:
    category: str
    name: str
    size: str
    id: str

    def __str__(self):
        return f'[{self.category}] {self.name} ({self.size}) [{self.id}]'


@dataclass
class ParseResult:
    next_page_url: str = field(default=None)
    rows: List[TorrentRow] = field(default_factory=list)


class Parser:
    def __init__(self, config):
        self.config = config

    def parse(self, page):
        result = ParseResult()

        tree = html.fromstring(page)
        try:
            result.next_page_url = self.config.BASE_URL \
                               + tree.xpath(self.config.NEXT_PAGE_SELECTOR)[0]
        except IndexError:
            pass

        rows = tree.xpath(self.config.ROW_SELECTOR)
        for row in rows:
            result.rows.append(TorrentRow(
                category=row.xpath(self.config.DATA_SELECTOR_CATEGORY)[0],
                name=row.xpath(self.config.DATA_SELECTOR_NAME)[0],
                size=row.xpath(self.config.DATA_SELECTOR_SIZE)[0],
                id=row.xpath(self.config.DATA_SELECTOR_ID)[0],
            ))
        return result


class Driver:
    def __init__(self, config, query, downloader, parser):
        self.config = config
        self.query = query
        self.downloader = downloader
        self.parser = parser

    def run(self):
        torrents = []
        url = self.config.first_page(self.query)
        while url:
            page = self.downloader.get(url)
            parse_result = self.parser.parse(page)
            torrents += parse_result.rows
            url = parse_result.next_page_url

        print(self.query.replace("\n", "???"))
        for torrent in torrents:
            print(torrent)


def run_parsing(config):
    if len(sys.argv) != 2:
        print("Too many or not enough arguments.", file=sys.stderr)
        print("Usage: ./watcher nyaa QUERY", file=sys.stderr)
        exit(1)

    query = sys.argv[1]
    down = Downloader()
    parser = Parser(config)
    d = Driver(config, query, down, parser)
    try:
        d.run()
    except Exception:
        traceback.print_exc()
        exit(1)
