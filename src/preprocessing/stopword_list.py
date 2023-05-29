from Sastrawi.StopWordRemover.StopWordRemoverFactory import StopWordRemoverFactory

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
