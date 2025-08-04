import pandas as pd
from typing import List
from .base_saver import BaseSaver

class JsonSaver(BaseSaver):
    @property
    def supported_extensions(self) -> List[str]:
        """JSON saver supports .json files"""
        return ['.json']

    def save(self, data: pd.DataFrame) -> None:
        data.to_json(self.filepath, orient='records', indent=2)