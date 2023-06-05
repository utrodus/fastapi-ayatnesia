import math

class TFIDF:
    # Function to calculate term frequency (TF)
    @staticmethod
    def calculate_tf(document : list, term : str):
        tf = document.count(term) / float(len(document))
        return tf

    # Function to calculate inverse document frequency (IDF)
    @staticmethod
    def calculate_idf(documents : list, term : str):
        num_documents_with_term = sum(1 for document in documents if term in document)
        if num_documents_with_term > 0:
            return 1.0 + math.log(float(len(documents) / (1 + num_documents_with_term)))
        else: 
            return 1.0
        
    # Function to calculate TF-IDF
    @staticmethod
    def calculate(document : list, documents: list, term : str):
        tf = TFIDF.calculate_tf(document, term)
        idf = TFIDF.calculate_idf(documents, term)
        tfidf = tf * idf
        return tfidf        