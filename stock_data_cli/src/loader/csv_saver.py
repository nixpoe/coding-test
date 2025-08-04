import pandas as pd
from typing import List
from .base_saver import BaseSaver

class CsvSaver(BaseSaver):
    @property
    def supported_extensions(self) -> List[str]:
        """CSV saver supports .csv files"""
        return ['.csv']

    def save(self, data: pd.DataFrame) -> None:
        data.to_csv(self.filepath, index=False)