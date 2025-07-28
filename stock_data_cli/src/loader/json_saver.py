class JsonSaver:
    def __init__(self, filepath):
        self.filepath = filepath

    def save(self, data):
        data.to_json(self.filepath, orient='records', lines=True)