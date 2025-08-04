import pandas as pd
from typing import List
from .base_loader import BaseLoader

class CsvLoader(BaseLoader):
    @property
    def supported_extensions(self) -> List[str]:
        """CSV loader supports .csv files"""
        return ['.csv']

    def load_data(self) -> pd.DataFrame:
        try:
            from .base_loader import REQUIRED_COLUMNS
            data = pd.read_csv(self.filepath, usecols=REQUIRED_COLUMNS)
            return data
        except Exception as e:
            print(f"Error loading CSV data: {e}")
            return None