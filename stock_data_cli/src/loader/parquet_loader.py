import pandas as pd
from typing import List
from .base_loader import BaseLoader

class ParquetLoader(BaseLoader):
    @property
    def supported_extensions(self) -> List[str]:
        """Parquet loader supports .parquet and .pq files"""
        return ['.parquet', '.pq']

    def load_data(self) -> pd.DataFrame:
        from .base_loader import REQUIRED_COLUMNS
        data = pd.read_parquet(self.filepath)
        data = data[REQUIRED_COLUMNS]
        return data