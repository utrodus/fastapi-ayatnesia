import json
from models.quran_model import quran_model_from_dict


class JSONReader:
    def __init__(self, file_path):
        """Init method for JSONReader class.
        This constructor takes a file path as an argument and assigns it to the file_path attribute.
        """
        self.file_path = file_path

    def read_json_file(self):
        """Reads the JSON file and returns the data.

        Returns:
        Object: The data from the JSON file.
        """
        with open(self.file_path, encoding="utf8") as f:
            data = json.load(f)
        return data

    def convert_to_list_of_dict(self):
        """Converts the JSON file to a list of dictionaries.

        Returns:
        List: The list of dictionaries.
        """
        read_results = self.read_json_file()
        quran_data = quran_model_from_dict(read_results)
        return quran_data
