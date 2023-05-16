
from nltk.tokenize import word_tokenize
import re
from Sastrawi.StopWordRemover.StopWordRemoverFactory import StopWordRemoverFactory
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
        stopword_factory = StopWordRemoverFactory()
        stopword_remover = stopword_factory.create_stop_word_remover()
        filtered_sentence_result = []
        for token in word_tokens:
            filtered_sentence = stopword_remover.remove(token)
            if(filtered_sentence != "" and filtered_sentence != ''):
                filtered_sentence_result.append(filtered_sentence)
        
        return filtered_sentence_result

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