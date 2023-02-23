from json_reader import get_quran_data
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import re
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory


class Preprocessing:
    def __init__(self, input_string):
        self.input_string = input_string

    def casefold_string(self):
        """Converts all the characters in the text to lowercase."""
        return self.input_string.lower()

    def tokenize_string(self):
        """Tokenizes the text."""
        remove_char = re.sub(r"[^\w]", " ", self.input_string)
        remove_number = "".join(filter(lambda x: not x.isdigit(), remove_char))
        word_tokens = word_tokenize(remove_number)
        return word_tokens

    def remove_stop_words(self, word_tokens):
        """Removes the stop words from the text."""
        stop_words = set(stopwords.words("indonesian"))
        filtered_sentence = [w for w in word_tokens if not w in stop_words]
        return filtered_sentence

    def stemming_text(self, word_tokens):
        """Stems the text."""
        stemmer = StemmerFactory().create_stemmer()
        stemming_results = []
        for token in word_tokens:
            stemming_ayat = stemmer.stem(token)
            stemming_results.append(stemming_ayat)
        return stemming_results

    def execute(self):
        """Preprocesses the query or qur'an data."""
        self.input_string = self.casefold_string()
        tokenize_result = self.tokenize_string()
        remove_stop_words_result = self.remove_stop_words(tokenize_result)
        stemming_result = self.stemming_text(remove_stop_words_result)
        return stemming_result


# preprocessing_result = Preprocessing(get_quran_data()[1].ayahs[6].translation).execute()
# print(preprocessing_result)


def preprocess_quran_data():
    """Preprocesses the qur'an data."""
    print("Preprocessing the qur'an data...")
    quran_data = get_quran_data()
    # create a list of dictionaries from the qur'an data preprocessed
    results = []
    # create a temporary list of dictionaries for ayahs
    temp_list_ayahs = []
    # create a temporary dictionary for surahs
    temp_dict_surah: dict = {}
    # create a temporary dictionary for ayahs
    temp_dict_ayahs: dict = {}
    # iterate through the qur'an data for preprocessing and store the results in the results list
    for surah in quran_data:
        print(f"#---Preprocessing surat: {surah.name}---#\n")
        temp_dict_surah.clear()
        for ayah in surah.ayahs:
            print(f"Preprocessing ayat - {ayah.number}\n")
            temp_list_ayahs.clear()
            preprocessing_result = Preprocessing(ayah.translation).execute()
            temp_dict_ayahs['number'] = ayah.number.to_dict()
            temp_dict_ayahs['arab'] = ayah.arab
            temp_dict_ayahs['preprocess_result'] = preprocessing_result
            temp_dict_ayahs['tafsir'] = ayah.tafsir.to_dict()
            temp_dict_ayahs['meta'] = ayah.meta.to_dict()
            temp_list_ayahs.append(temp_dict_ayahs)
            # print(preprocessing_result, "\n")
            # ayah.translation = preprocessing_result
        temp_dict_surah['number'] = surah.number
        temp_dict_surah['numberOfAyahs'] = surah.number_of_ayahs
        temp_dict_surah['name'] = surah.name
        temp_dict_surah['translation'] = surah.translation
        temp_dict_surah['ayahs'] = temp_list_ayahs
        results.append(temp_dict_surah)
    print("\nPreprocessing the qur'an data is done.!\n")
    return results


preprocess_quran_data()

