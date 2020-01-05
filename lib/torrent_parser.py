import requests
from lxml import html
import sys
from copy import copy


class TorrentParser:
    def __init__(self, parsing_data):
        self.parsing_data = parsing_data
        try:
            self.query = self.parsing_data['args'][1]
        except Exception as e:
            print(e, file=sys.stderr)
            exit(1)

        self.results = []
        self.tree = None
        self.is_next_page = True
        self.next_page_url = None

    def get_tree(self):
        if not self.next_page_url:
            r = requests.get(self.parsing_data['search_url'] +
                             self.query)
        else:
            r = requests.get(self.parsing_data["base_url"] + self.next_page_url)
        self.tree = html.fromstring(r.text)

    def get_next_page_url(self):
        try:
            self.next_page_url = self.tree.xpath(self.parsing_data['next_page_selector'])[0]
        except:
            self.is_next_page = False
        self.parsing_data["search_url"] = self.next_page_url

    def get_rows(self):
        self.get_tree()
        return self.tree.xpath(self.parsing_data["row_selector"])

    def parse_row_data(self):
        data_dict = {
            "category": None,
            "name": None,
            "size": None,
        }
        rows = self.get_rows()
        for row in rows:
            row_data_dict = copy(data_dict)
            for key in self.parsing_data["data_selectors"]:
                if self.parsing_data["data_selectors"][key]:
                    row_data_dict[key] = row.xpath(self.parsing_data
                                                   ["data_selectors"][key])[0]
            self.results.append(row_data_dict)

    def format_output(self):
        print(self.query.replace("\n", "???"))
        for result in self.results:
            print(f"[{result['category']}] {result['name']} ({result['size']})")


def run_parsing(parsing_data: dict):
    parser = TorrentParser(parsing_data)
    while parser.is_next_page:
        parser.parse_row_data()
        parser.get_next_page_url()
    parser.format_output()
