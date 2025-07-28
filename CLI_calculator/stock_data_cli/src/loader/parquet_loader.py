import pandas as pd

REQUIRED_COLUMNS = ['unadjusted_close', 'ticker_symbol', 'datetime', 'split', 'dividend']

class ParquetLoader:
    def __init__(self, filepath):
        self.filepath = filepath

    def load_data(self):
        data = pd.read_parquet(self.filepath)
        data = data[REQUIRED_COLUMNS]
        return data