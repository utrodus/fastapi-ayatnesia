from json_reader import JSONReader
from preprocessing import Preprocessing
import json


def get_quran_data():
    """Returns the data from the JSON file."""
    file_path = "data/raw_data/quran.json"
    json_reader = JSONReader(file_path)
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
                    "arab": ayah.arab,
                    "preprocess_result": preprocessing_result,
                    "tafsir": ayah.tafsir.to_dict(),
                    "meta": ayah.meta.to_dict(),
                }
            )
        results.append(
            {
                "name": surah.name,
                "number": surah.number,
                "numberOfAyahs": surah.number_of_ayahs,
                "translation": surah.translation,
                "ayahs": temp_list_ayahs,
            }
        )
        

    print("\nPreprocessing the qur'an data is done.!\n")
    return results


def write_quran_preprocess_result_to_file():
    """Writes the qur'an data preprocessed to a JSON file."""
    print("Writing the qur'an data preprocessed to a JSON file...")
    quran_data_preprocessed = preprocess_quran_data()

    with open("data/preprocessed_data/quran_preprocessed.json", "w") as f:
        json.dump(quran_data_preprocessed, f)
    print("\nWriting the qur'an data preprocessed to a JSON file is done.!\n")


# write_quran_preprocess_result_to_file()
write_quran_preprocess_result_to_file()
