from lib.downloader import Downloader
import sys
from lxml import etree
import base64


class Parser:

    def parse_xml(self, page, xpath):
        tree = etree.fromstring(page)
        tree = self._strip_namespaces(tree)
        return [elem.text for elem in tree.xpath(xpath)]

    def _strip_namespaces(self, tree):
        for element in tree.xpath('descendant-or-self::*'):
            if element.prefix:
                raise Exception("Foobar")
            element.tag = etree.QName(element).localname
        return tree


class Driver:

    def run(self, url, xpath):
        page = Downloader.get(url).encode('ascii')
        results = Parser().parse_xml(page, xpath)
        print(self._result_id(url, xpath))
        for result in results:
            print(result)

    def _result_id(self, url, xpath):
        return str(base64.urlsafe_b64encode(f'{url}{xpath}'.
                                            encode("utf-8")), "utf-8")


def run_parsing():
    if len(sys.argv) != 3:
        print("Too many or not enough arguments.", file=sys.stderr)
        print("Usage: ./watcher xpath url xpath", file=sys.stderr)
        exit(1)

    try:
        xpath = etree.XPath(sys.argv[2])
    except (etree.XPathSyntaxError, etree.XPathEvalError):
        print("Not a valid XPATH", file=sys.stderr)
        exit(1)

    url = sys.argv[1]
    xpath = sys.argv[2]
    Driver().run(url, xpath)

