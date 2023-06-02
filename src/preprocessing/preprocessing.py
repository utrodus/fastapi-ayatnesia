from nltk.tokenize import word_tokenize
import re
from Sastrawi.StopWordRemover.StopWordRemoverFactory import StopWordRemoverFactory
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory

class StopwordList:
    """ This class contains the stopword list that will be used in the preprocessing step."""
    def __init__(self):
        self.stopword_factory = StopWordRemoverFactory()
        self.list_stopwords = self.stopword_factory.get_stop_words()
        ignored_stopword_list = ['demi', 'masa', 'kamu',  'menjawab', 'bulan', 'bertanya-tanya', 'hari', 'besar', 
                                 'melihatnya', 'dia', 'tidak', 'sesuatu', 'sekali-kali', 'mengetahui', 'pasti', 'mengerjakan',
                                 'nya', 'mereka', 'sendiri', 'bahwa', 'kami', 'melihat', 'lebih', 'dekat', 'kepadanya', 'daripada', 'apa',
                                 'saling', 'mengira', 'dengan', 'jelas', 'hanyalah', 'ibu', 'bapak', 'mata', 'kadar', 'memberi'
                               ]
        try:
            for stopword in ignored_stopword_list:
                self.list_stopwords.remove(stopword)
        except ValueError:
            print("Error: Stopword not found in list")                                
    
    def get_stopword_list(self):
        return self.list_stopwords


class Preprocessing:
    """ This class preprocesses the query or qur'an data. with the following steps:
    1. Casefolding
    2. Tokenization
    3. Stopword Removal
    4. Stemming
    """
    def __init__(self, input_string):        
        self.input_string = input_string
        stopword_list = StopwordList()
        self.stopword_list = stopword_list.get_stopword_list()                

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
        filtered_sentence_result = [w for w in word_tokens if not w in self.stopword_list]        
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
