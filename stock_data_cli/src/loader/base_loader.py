from abc import ABC, abstractmethod
from typing import List
import pandas as pd

REQUIRED_COLUMNS = ['unadjusted_close', 'ticker_symbol', 'datetime', 'split', 'dividend']

class BaseLoader(ABC):
    """Abstract base class for data loaders implementing Strategy pattern"""
    
    def __init__(self, filepath: str):
        self.filepath = filepath
    
    @property
    @abstractmethod
    def supported_extensions(self) -> List[str]:
        """Return list of file extensions this loader supports (e.g., ['.csv', '.txt'])"""
        pass
    
    @abstractmethod
    def load_data(self) -> pd.DataFrame:
        """Load data from file and return DataFrame with required columns"""
        pass
    
    def can_handle(self, file_extension: str) -> bool:
        """Check if this loader can handle the given file extension"""
        return file_extension.lower() in [ext.lower() for ext in self.supported_extensions]
    
    @classmethod
    def get_loader_for_file(cls, filepath: str) -> 'BaseLoader':
        """Factory method to get appropriate loader for file extension"""
        import os
        file_extension = os.path.splitext(filepath)[1]
        
        # Import here to avoid circular imports
        from .csv_loader import CsvLoader
        from .json_loader import JsonLoader  
        from .parquet_loader import ParquetLoader
        
        loaders = [CsvLoader, JsonLoader, ParquetLoader]
        
        for loader_class in loaders:
            loader_instance = loader_class(filepath)
            if loader_instance.can_handle(file_extension):
                return loader_instance
        
        raise ValueError(f"No loader found for file extension: {file_extension}")
