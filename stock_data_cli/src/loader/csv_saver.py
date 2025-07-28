class CsvSaver:
    def __init__(self, filepath):
        self.filepath = filepath

    def save(self, data):
        data.to_csv(self.filepath, index=False)