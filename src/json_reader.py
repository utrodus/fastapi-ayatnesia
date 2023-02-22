import json

class JSONReader:
    def __init__(self, file_path):
        self.file_path = file_path

    def read(self):
        with open(self.file_path,  encoding="utf8") as f:
            data = json.load(f)
        return data
