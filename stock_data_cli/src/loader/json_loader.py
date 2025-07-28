import pandas as pd

REQUIRED_COLUMNS = ['unadjusted_close', 'ticker_symbol', 'datetime', 'split', 'dividend']

class JsonLoader:
    def __init__(self, filepath):
        self.filepath = filepath

    def load_data(self):
        data = pd.read_json(self.filepath)
        data = data[REQUIRED_COLUMNS]
        return data