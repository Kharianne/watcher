import requests


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
