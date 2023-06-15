import sys
import os
sys.path.append("src")
import compress_fasttext
import numpy as np
from database.database import get_all_ayahs, save_word_embedding_result

class WordEmbedding:
    def __init__(self):
        self.model = self.load_model()
    
    def load_model(self):
        current_directory = os.path.dirname(__file__)
        pretrained_model_path = os.path.abspath(os.path.join(current_directory, 'pretrained_model/cc.id.300.small.bin'))
        model = compress_fasttext.models.CompressedFastTextKeyedVectors.load(pretrained_model_path)
        return model
    
    def get_nearest_words(self, words, topn=10):
        similar_words = []
        for word in words:
            if word in self.model:
                similar = self.model.similar_by_word(word, topn=topn)
                similar_words.extend([word[0] for word in similar])
        return similar_words
    

    def calculate_similarity(self, query, document):    
        query_vec = np.mean(self.model[query], axis=0)
        document_vec = np.mean(self.model[document], axis=0)
        similarities = self.model.cosine_similarities(query_vec, [document_vec])
        similarity = similarities[0]
        return similarity

class WordEmbeddingAyahs:
    def __init__(self):
        self.all_ayahs = get_all_ayahs()
        self.word_embedding = WordEmbedding()
        self.get_word_ayah_nearest_words()
            
    def get_word_ayah_nearest_words(self):
        document_words = []
        for i, doc in enumerate(self.all_ayahs):
            document_words.append(self.word_embedding.get_nearest_words(doc['preprocessed']))
            print(f"Processed {i+1} of {len(self.all_ayahs)} ayahs")
        for i, doc in enumerate(document_words):
            save_word_embedding_result(i+1, doc)
        
# uncomment this line to run the script for word embedding quran ayahs and save the result to database
# WordEmbeddingAyahs()