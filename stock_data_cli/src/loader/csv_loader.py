import pandas as pd

REQUIRED_COLUMNS = ['unadjusted_close', 'ticker_symbol', 'datetime', 'split', 'dividend']

class CsvLoader:
    def __init__(self, filepath, columns=None):
        self.filepath = filepath

    def load_data(self):
        try:
            data = pd.read_csv(self.filepath, usecols=REQUIRED_COLUMNS)
            return data
        except Exception as e:
            print(f"Error loading CSV data: {e}")
            return None