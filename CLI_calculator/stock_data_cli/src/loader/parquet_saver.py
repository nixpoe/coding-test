class ParquetSaver:
    def __init__(self, filepath):
        self.filepath = filepath

    def save(self, data):
        data.to_parquet(self.filepath, index=False)