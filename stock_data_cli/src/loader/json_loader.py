import pandas as pd
from typing import List
from .base_loader import BaseLoader

class JsonLoader(BaseLoader):
    @property
    def supported_extensions(self) -> List[str]:
        """JSON loader supports .json files"""
        return ['.json']

    def load_data(self) -> pd.DataFrame:
        from .base_loader import REQUIRED_COLUMNS
        data = pd.read_json(self.filepath)
        data = data[REQUIRED_COLUMNS]
        return data