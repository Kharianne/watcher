import base64
import os
import pickle
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
    continue_searching: bool = field(default=True)


class Parser:
    def __init__(self, config):
        self.config = config

    def parse(self, page, latest_id):
        result = ParseResult()

        tree = html.fromstring(page)
        try:
            result.next_page_url = self.config.BASE_URL \
                               + tree.xpath(self.config.NEXT_PAGE_SELECTOR)[0]
        except IndexError:
            pass

        rows = tree.xpath(self.config.ROW_SELECTOR)
        for row in rows:
            if (_id := row.xpath(self.config.DATA_SELECTOR_ID)[0]) == \
                    latest_id:
                result.continue_searching = False
                break
            result.rows.append(TorrentRow(
                category=row.xpath(self.config.DATA_SELECTOR_CATEGORY)[0],
                name=row.xpath(self.config.DATA_SELECTOR_NAME)[0],
                size=row.xpath(self.config.DATA_SELECTOR_SIZE)[0],
                id=_id,
            ))
        return result


class Driver:
    def __init__(self, config, query, downloader, parser):
        self.config = config
        self.query = query
        self.downloader = downloader
        self.parser = parser

    def _safe_name(self, name):
        return str(base64.urlsafe_b64encode(name.encode("utf-8")), "utf-8")

    def _pickle_name(self):
        subdir = self._safe_name(self.config.BASE_URL)
        fname = self._safe_name(self.query)
        return f'{self.config.store_base}/torrents/{subdir}/{fname}'

    def _load_pickle(self):
        try:
            with open(self._pickle_name(), 'rb') as f:
                return pickle.load(f)
        except FileNotFoundError:
            return []

    def _save_pickle(self, torrents):
            dir = os.path.dirname(self._pickle_name())
            os.makedirs(dir, exist_ok=True)
            with open(self._pickle_name(), 'wb') as f:
                pickle.dump(torrents, f)

    def run(self):
        storage = self._load_pickle()
        try:
            latest_id = storage[0].id
        except IndexError:
            latest_id = None

        torrents = []
        url = self.config.first_page(self.query)
        continue_searching = True
        while url and continue_searching:
            page = self.downloader.get(url)
            parse_result = self.parser.parse(page, latest_id)
            torrents += parse_result.rows
            continue_searching = parse_result.continue_searching
            url = parse_result.next_page_url

        try:
            storage = torrents + storage
        except TypeError:
            storage = torrents

        print(self.query.replace("\n", "???"))
        for row in storage:
            print(row)

        self._save_pickle(storage)


def run_parsing(config):
    if len(sys.argv) != 2:
        print("Too many or not enough arguments.", file=sys.stderr)
        print("Usage: ./watcher nyaa QUERY", file=sys.stderr)
        exit(1)

    try:
        config.store_base = os.environ['WATCHER_STORE']
    except:
        print("Env variable WATCHER_STORE is missing!", file=sys.stderr)
        exit(1)

    query = sys.argv[1]
    down = Downloader()
    parser = Parser(config)
    d = Driver(config, query, down, parser)
    try:
        d.run()
    except:
        traceback.print_exc()
        exit(1)
