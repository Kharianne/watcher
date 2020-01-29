import base64
import os
import pickle


class Pickling:
    def __init__(self, name, config):
        self.name = name
        self.config = config

    def _safe_name(self, name):
        return str(base64.urlsafe_b64encode(name.encode("utf-8")), "utf-8")

    def _pickle_name(self):
        subdir = self._safe_name(self.config.BASE_URL)
        fname = self._safe_name(self.name)
        return f'{self.config.store_base}/torrents/{subdir}/{fname}'

    def load_pickle(self):
        try:
            with open(self._pickle_name(), 'rb') as f:
                return pickle.load(f)
        except FileNotFoundError:
            return []

    def save_pickle(self, torrents):
            dir = os.path.dirname(self._pickle_name())
            os.makedirs(dir, exist_ok=True)
            with open(self._pickle_name(), 'wb') as f:
                pickle.dump(torrents, f)