from json_reader import JSONReader
from preprocessing import Preprocessing
from db_helper import write_quran_db
import os

current_path = os.path.join(os.path.dirname(os.path.realpath(__file__)))
quran_json_path = os.path.abspath(os.path.join(current_path, "data/quran.json"))

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
        for ayah in surah.ayahs:
            # print(f"Preprocessing ayat - {ayah.number.in_surah} \n")
            preprocessing_result = Preprocessing(ayah.translation).execute()
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

    write_quran_db(results)
    print("\nPreprocessing the qur'an data is done.!\n")


preprocess_quran_data()
