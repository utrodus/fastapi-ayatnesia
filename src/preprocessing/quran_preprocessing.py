import sys
sys.path.append("src")
from json_reader import JSONReader
from database import database as db
from preprocessing import Preprocessing
import os

quran_json_path = os.path.abspath(os.path.join("src/datasets/quran.json"))

def get_quran_data():
    """Returns the data from the JSON file."""
    json_reader = JSONReader(quran_json_path)
    quran_data = json_reader.convert_to_list_of_dict()
    return quran_data


def preprocess_quran_data():
    """Preprocesses the qur'an data."""
    print("Preprocessing the qur'an data...")
    quran_data = get_quran_data()  # create a list of ayahs for each surah temporarily
    temp_list_ayahs = []
    # create a list of dictionaries from the qur'an data preprocessed
    results = []

    # iterate through the qur'an data for preprocessing and store the results in the results list
    
    for surah in quran_data:
        print(f"## Preprocessing surat: {surah.name} \n")
        # print(f"Number of ayahs: {len(surah.ayahs)} \n")
        
        for ayah in surah.ayahs:
            preprocessing_result = Preprocessing(ayah.translation).execute()
            # check if ayah added to the list of ayahs
            if ayah not in temp_list_ayahs:
                temp_list_ayahs.append(
                {
                    "number": ayah.number.to_dict(),
                    "arabic": ayah.arab,
                    "preprocced": preprocessing_result,
                    "translation": ayah.translation,    
                    "tafsir": ayah.tafsir.kemenag.short,
                }
            )
                                  
        results.append(
                {
                    "name": surah.name,
                    "number": surah.number,
                    "translation": surah.translation,
                    "ayahs": temp_list_ayahs,
                }
            )
        if(temp_list_ayahs != []):
            temp_list_ayahs = []  
           
                            
    db.write_quran_db(results)
    print("\nPreprocessing the qur'an data is done.!\n")


preprocess_quran_data()
