import numpy as np
import math
import pandas as pd

class CosineSimilarity:
    def __init__(self, query, doc_num, tfidf_dict_qry, document_frequency, tfidf_dict_doc):
        """
        Menginisialisasi kelas CosineSimilarity.

        Args:
            quran_documents (list): Sebuah daftar dokumen Quran.
            query (str): String query untuk perhitungan similaritas cosine.
        """
        self.query = query
        self.doc_num = doc_num
        self.tfidf_dict_qry = tfidf_dict_qry
        self.document_frequency = document_frequency
        self.tfidf_dict_doc = tfidf_dict_doc
    
    def cosine_similarity(self, vector1, vector2):
        """
        Menghitung similaritas cosine antara dua vektor.

        Args:
            vector1 (np.array): Vektor pertama.
            vector2 (np.array): Vektor kedua.

        Returns:
            float: Similaritas cosine antara dua vektor.
        """
        dot_product = np.dot(vector1, vector2)
        norm_vector1 = np.linalg.norm(vector1)
        norm_vector2 = np.linalg.norm(vector2)
        return dot_product / (norm_vector1 * norm_vector2)