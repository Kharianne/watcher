import requests
from lxml import html
import sys
import json


class TorrentParser:
    def __init__(self, parsing_data):
        self.parsing_data = parsing_data
        if len(self.parsing_data['args']) > 2:
            raise TypeError(f'Expected 1 query argument got '
                            f'{len(self.parsing_data["args"])-1}')
        try:
            self.query = self.parsing_data['args'][1]
        except Exception as e:
            print(e, file=sys.stderr)
            exit(1)

        self.results = []
        self.tree = None
        self.has_next_page = True
        self.next_page_url = None

    def get_tree(self):
        try:
            if not self.next_page_url:
                r = requests.get(self.parsing_data['search_url'] +
                                 self.query)
            else:
                r = requests.get(self.parsing_data["base_url"] +
                                 self.next_page_url)
        except Exception as e:
            print(f'Could not connect to host: {e}', file=sys.stderr)
            exit(1)
        else:
            if r.status_code == 200:
                self.tree = html.fromstring(r.text)
            else:
                raise Exception(f'Request ended with status code: '
                                f'{r.status_code}')

    def get_next_page_url(self):
        try:
            self.next_page_url = self.tree.xpath(
                self.parsing_data['next_page_selector'])[0]
        except IndexError:
            self.has_next_page = False
        # FIXME: This is fucking useless
        # self.parsing_data["search_url"] = self.next_page_url

    def get_rows(self):
        self.get_tree()
        return self.tree.xpath(self.parsing_data["row_selector"])

    def read_rows_until(self, last_id):
        rows = self.get_rows()
        for row in rows:
            data_dict = {
                "category": None,
                "name": None,
                "size": None,
                "id": None
            }
            for key in self.parsing_data["data_selectors"]:
                if self.parsing_data["data_selectors"][key]:
                    data_dict[key] = row.xpath(self.parsing_data
                                                   ["data_selectors"][key])[0]
            if data_dict["id"] == last_id:
                return False
            else:
                print(data_dict)
                self.results.append(data_dict)
        return True

    def format_output(self):
        print(self.query.replace("\n", "???"))
        for result in self.results:
            print(f"[{result['id']}][{result['category']}] {result['name']} "
                  f"({result['size']})")


def run_parsing(parser_config: dict):
    with open('storage.json', "r", encoding='utf-8') as f:
        parser = TorrentParser(parser_config)
        storage = json.load(f)
        # TODO: use .get()
        try:
            last_id = storage[parser.query]["last_id"]
        except KeyError:
            last_id = None

        res = True
        while parser.has_next_page and res:
            res = parser.read_rows_until(last_id)
            parser.get_next_page_url()

        if parser.query not in storage.keys():
            storage.update({parser.query: {
                "results": parser.results,
                "last_id": parser.results[0]["id"] if len(parser.results) > 0
                else None
            }})
        else:
            storage[parser.query]["results"] = \
                parser.results + storage[parser.query]["results"]
            if len(parser.results) > 0:
                storage[parser.query]["last_id"] = parser.results[0]["id"]

        print(len(storage[parser.query]["results"]))

    with open('storage.json', "w", encoding='utf-8') as f:
        json.dump(storage, f)
