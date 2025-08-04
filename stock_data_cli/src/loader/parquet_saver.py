import pandas as pd
from typing import List
from .base_saver import BaseSaver

class ParquetSaver(BaseSaver):
    @property
    def supported_extensions(self) -> List[str]:
        """Parquet saver supports .parquet and .pq files"""
        return ['.parquet', '.pq']

    def save(self, data: pd.DataFrame) -> None:
        data.to_parquet(self.filepath, index=False)