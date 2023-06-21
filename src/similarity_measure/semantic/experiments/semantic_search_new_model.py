# import os
# import sys
# sys.path.append("src")
# import numpy as np
# from gensim.models import FastText
# from database.database import get_all_ayahs
# import time

# # Load model word embedding FastText
# model_path = 'fasttext_quran_model.bin'

# current_directory = os.path.dirname(__file__)
# trained_model_path = os.path.abspath(os.path.join(current_directory, '../trained_model/fasttext_quran_model.bin'))
# model = FastText.load(trained_model_path)

# # Fungsi untuk menghitung cosine similarity antara vektor query dan vektor dokumen
# def calculate_similarity(query, document):
#     query_vector = np.mean([model.wv.get_vector(token) for token in query], axis=0)
#     document_vector = np.mean([model.wv.get_vector(token) for token in document], axis=0)

#     dot_product = np.dot(query_vector, document_vector)
#     query_norm = np.linalg.norm(query_vector)
#     document_norm = np.linalg.norm(document_vector)

#     similarity = dot_product / (query_norm * document_norm)
#     return similarity

# # Fungsi untuk mencari ayat yang paling relevan dengan query
# def search_ayah(query):
#     ayahs = get_all_ayahs()  # Ganti dengan fungsi yang mengambil data ayat dari database

#     results = []
#     for ayah in ayahs:
#         similarity = calculate_similarity(query, ayah['preprocessed'])
#         results.append((ayah['id'], similarity, ayah['arabic'], ayah['translation']))

#     results = sorted(results, key=lambda x: x[1], reverse=True)
#     return results

# start = time.time()
# # Contoh penggunaan
# query = ['istimewa', 'hewan', 'ternak', 'alquran']
# results = search_ayah(query)
# top_results = results[:10]  # Ambil hanya 10 hasil teratas

# for result in top_results:
#     ayah_id = result[0]
#     similarity = result[1]
#     arabic_ayah = result[2]
#     translation_ayah = result[3]
#     print(f"Ayat ID: {ayah_id}, Similarity: {similarity}")
#     print(f"Arabic Ayah: {arabic_ayah}")
#     print(f"Translation: {translation_ayah}")
#     print()
    
# end = time.time()
# print(f'Finished in {end - start} seconds')


import os
import sys
sys.path.append("src")
import numpy as np
from gensim.models import FastText
from database.database import get_all_ayahs
import time

# Load model word embedding FastText
model_path = 'fasttext_quran_model.bin'

current_directory = os.path.dirname(__file__)
trained_model_path = os.path.abspath(os.path.join(current_directory, '../trained_model/fasttext_quran_model.bin'))
model = FastText.load(trained_model_path)

# Function to calculate cosine similarity between query and document vectors
def calculate_similarity(query, document):
    query_vector = np.mean([model.wv.get_vector(token) for token in query], axis=0)
    document_vector = np.mean([model.wv.get_vector(token) for token in document], axis=0)

    dot_product = np.dot(query_vector, document_vector)
    query_norm = np.linalg.norm(query_vector)
    document_norm = np.linalg.norm(document_vector)

    similarity = dot_product / (query_norm * document_norm)
    return similarity

# Function to search for most relevant ayahs with the given query
def search_ayah(query):
    ayahs = get_all_ayahs()  # Replace with a function that retrieves ayahs from the database

    results = []
    for ayah in ayahs:
        similarity = calculate_similarity(query, ayah['preprocessed'])
        results.append({
            'ayah_id': ayah['id'],
            'similarity': similarity,
            'arabic_ayah': ayah['arabic'],
            'translation_ayah': ayah['translation']
        })

    results = sorted(results, key=lambda x: x['similarity'], reverse=True)
    return results

# Function to get the top results as a list of dictionaries
def get_top_results(query, num_results=10):
    results = search_ayah(query)
    top_results = results[:num_results]
    return top_results

start = time.time()

# Example usage
query = ['istimewa', 'hewan', 'ternak', 'alquran']
top_results = get_top_results(query)

for result in top_results:
    ayah_id = result['ayah_id']
    similarity = result['similarity']
    arabic_ayah = result['arabic_ayah']
    translation_ayah = result['translation_ayah']
    print(f"Ayat ID: {ayah_id}, Similarity: {similarity}")
    print(f"Arabic Ayah: {arabic_ayah}")
    print(f"Translation: {translation_ayah}")
    print()

end = time.time()
print(f'Finished in {end - start} seconds')
