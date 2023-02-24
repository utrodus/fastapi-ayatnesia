
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


