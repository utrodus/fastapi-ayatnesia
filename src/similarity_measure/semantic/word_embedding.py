import sys
import os
sys.path.append("src")
import compress_fasttext
import numpy as np

class WordEmbedding:
    def __init__(self):
        current_directory = os.path.dirname(__file__)          
        trained_model_path = os.path.abspath(os.path.join(current_directory, 'trained_model/cc.id.300.small.bin'))
        self.model = compress_fasttext.models.CompressedFastTextKeyedVectors.load(trained_model_path)
            
    def get_words_vector(self, data: list ):
        words_vector_result =  np.mean([self.model.get_vector(token) for token in data], axis=0)
        return words_vector_result
    
    def calculate_similarity(self, query_vector, ayahs_vector):
        dot_product = np.dot(query_vector, ayahs_vector)
        query_norm = np.linalg.norm(query_vector)
        document_norm = np.linalg.norm(ayahs_vector)
        similarity = dot_product / (query_norm * document_norm)
        return similarity        
