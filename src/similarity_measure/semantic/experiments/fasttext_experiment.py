import sys
import os
sys.path.append("src")
import compress_fasttext

from gensim.models.fasttext import load_facebook_vectors, load_facebook_model
import numpy as np

current_directory = os.path.dirname(__file__)

pretrained_model_path = os.path.abspath(os.path.join(current_directory, '../pretrained_model/cc.id.300.bin'))
small_pretrained_model_path = os.path.abspath(os.path.join(current_directory, '../pretrained_model/cc.id.300.small.bin'))

model = load_facebook_vectors(pretrained_model_path)
# small_model = compress_fasttext.models.CompressedFastTextKeyedVectors.load(small_pretrained_model_path)

nearest_words = model.most_similar("tunjuk", topn=15)
print(nearest_words)

# # Fungsi untuk mendapatkan kata-kata terdekat dari dokumen/query
# def get_similar_words(text):
#     similar_words = []
#     for word in text.split():
#         try:
#             similar = model.most_similar(word, topn=5)  # Ambil 5 kata terdekat
#             similar_words.extend([word[0] for word in similar])
#         except KeyError:
#             continue
#     return similar_words

# # Fungsi untuk menghitung kemiripan semantik menggunakan Jaccard Measure
# def semantic_similarity(query, document):
#     query_words = set(get_similar_words(query))
#     document_words = set(get_similar_words(document))
    
#     intersection = len(query_words.intersection(document_words))
#     union = len(query_words) + len(document_words) - intersection
    
#     similarity = intersection / union
#     return similarity

# # Contoh penggunaan
# query = "jembatan yang lurus"
# document = "Tunjukilah kami jalan yang lurus, (yaitu) jalan orang-orang yang telah Engkau beri nikmat kepadanya; bukan (jalan) mereka yang dimurkai, dan bukan (pula jalan) mereka yang sesat."

# similarity_score = semantic_similarity(query, document)
# print("Kemiripan semantik:", similarity_score)