import json


class JSONReader:
    def __init__(self, file_path):
        """Init method for JSONReader class. 
        This constructor takes a file path as an argument and assigns it to the file_path attribute.
        """
        self.file_path = file_path

    def read(self):
        """Reads the JSON file and returns the data.
        
        Returns: 
        Object: The data from the JSON file.
        """        """"""
        with open(self.file_path, encoding="utf8") as f:
            data = json.load(f)
        return data
