from json_reader import JSONReader
from models.quran_model import quran_model_from_dict

def preprocessing():
    json_reader = JSONReader("data/raw_data/quran.json")
    quran_data = quran_model_from_dict(json_reader.read())
    return quran_data