from abc import ABC, abstractmethod
from typing import List
import pandas as pd

class BaseSaver(ABC):
    """Abstract base class for data savers implementing Strategy pattern"""
    
    def __init__(self, filepath: str):
        self.filepath = filepath
    
    @property
    @abstractmethod
    def supported_extensions(self) -> List[str]:
        """Return list of file extensions this saver supports (e.g., ['.csv', '.txt'])"""
        pass
    
    @abstractmethod
    def save(self, data: pd.DataFrame) -> None:
        """Save DataFrame to file"""
        pass
    
    def can_handle(self, file_extension: str) -> bool:
        """Check if this saver can handle the given file extension"""
        return file_extension.lower() in [ext.lower() for ext in self.supported_extensions]
    
    @classmethod
    def get_saver_for_file(cls, filepath: str) -> 'BaseSaver':
        """Factory method to get appropriate saver for file extension"""
        import os
        file_extension = os.path.splitext(filepath)[1]
        
        # Import here to avoid circular imports
        from .csv_saver import CsvSaver
        from .json_saver import JsonSaver
        from .parquet_saver import ParquetSaver
        
        savers = [CsvSaver, JsonSaver, ParquetSaver]
        
        for saver_class in savers:
            saver_instance = saver_class(filepath)
            if saver_instance.can_handle(file_extension):
                return saver_instance
        
        raise ValueError(f"No saver found for file extension: {file_extension}")
