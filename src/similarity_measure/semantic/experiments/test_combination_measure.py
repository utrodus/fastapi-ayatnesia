import os
import compress_fasttext
import numpy as np

# Step 1: Mendapatkan kata-kata terdekat tiap kata dari dokumen dan query
def get_most_similar_words(model, words, topn=100):
    word_vectors = model
    similar_words = []
    for word in words:
        if word in word_vectors:
            similar = word_vectors.similar_by_word(word, topn=topn)
            similar_words.extend([word[0] for word in similar])
    return similar_words

current_directory = os.path.dirname(__file__)
pretrained_model_path = os.path.abspath(os.path.join(current_directory, '../pretrained_model/cc.id.300.small.bin'))
model = compress_fasttext.models.CompressedFastTextKeyedVectors.load(pretrained_model_path)

# Query
query = ['dengan', 'nama', 'allah', 'maha', 'asih', 'maha', 'sayang']

# Documents
documents = [
    {'preprocessed': ['dengan', 'nama', 'allah', 'maha', 'asih', 'maha', 'sayang']},
    {'preprocessed': ['puji', 'allah', 'tuhan', 'alam']},
    {'preprocessed': ['maha', 'asih', 'maha', 'sayang']},
    {'preprocessed': ['milik', 'hari', 'balas']},
    {'preprocessed': ['engkau', 'kami', 'sembah', 'engkau', 'kami', 'tolong']},
    {'preprocessed': ['tunjuk', 'kami', 'jalan', 'lurus']},
    {'preprocessed': ['jalan', 'engkau', 'nikmat', 'kepada', 'jalan', 'mereka', 'murka', 'jalan', 'mereka', 'sesat']},
    # {'preprocessed': ['alif','lam', 'mim']}
]

# Step 1: Mendapatkan kata-kata terdekat tiap kata dari dokumen dan query
query_words = get_most_similar_words(model, query)
document_words = []
for doc in documents:
    doc_words = get_most_similar_words(model, doc['preprocessed'])
    document_words.append(doc_words)

# Step 2: Menghitung cosine similarity menggunakan model.cosine_similarities()
def calculate_cosine_similarity(query, document):    
    query_vec = np.mean(model[query], axis=0)
    document_vec = np.mean(model[document], axis=0)
    similarity = np.dot(query_vec, document_vec) / (np.linalg.norm(query_vec) * np.linalg.norm(document_vec))
    return similarity

# Step 3: Menghitung Jaccard similarity
def calculate_jaccard_similarity(query, document):
    query_set = set(query)
    document_set = set(document)
    intersection = query_set.intersection(document_set)
    union = query_set.union(document_set)
    similarity = len(intersection) / len(union)
    return similarity

# Step 4: Menggabungkan cosine similarity dan Jaccard similarity dengan Weighted Average
def calculate_similarity(query, document, w1, w2):    
    cosine_sim = calculate_cosine_similarity(query, document)
    jaccard_sim = calculate_jaccard_similarity(query, document)
    similarity = (w1 * cosine_sim + w2 * jaccard_sim) / (w1 + w2)
    return similarity

# Step 5: Perhitungan kemiripan semantik
similarities = []
w1 = 0.8  # Bobot untuk cosine similarity
w2 = 0.2  # Bobot untuk Jaccard similarity

for i, doc_words in enumerate(document_words):
    similarity = calculate_similarity(query_words, doc_words, w1, w2)
    similarities.append(similarity)

# Step 6: Mengurutkan dokumen berdasarkan kemiripan tertinggi
sorted_documents = sorted(zip(documents, similarities), key=lambda x: x[1], reverse=True)

for doc, similarity in sorted_documents:
    similarity_percentage = similarity * 100
    print(f"Similarity with document: {similarity}")
    print(f"Similarity percentage: {similarity_percentage:.3f}%")
    print(f"Preprocessed Document: {doc['preprocessed']}")
    print("------------")