
import os
import compress_fasttext
import numpy as np


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
    {'preprocessed': ['alif','lam', 'mim']}
]

# Step 1: Mendapatkan kata-kata terdekat tiap kata dari dokumen dan query
def get_most_similar_words(model, words, topn=100):
    word_vectors = model
    similar_words = []
    for word in words:
        if word in word_vectors:
            similar = word_vectors.similar_by_word(word, topn=topn)
            similar_words.extend([word[0] for word in similar])
    return similar_words

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
    similarities = model.cosine_similarities(query_vec, [document_vec])
    similarity = similarities[0]
    return similarity

# Step 2.1: Pengukuran Kemiripan Kata antara query dan dokumen
sim_q_docs = []
for doc_words in document_words:
    sim_q_doc = calculate_cosine_similarity(query_words, doc_words)
    sim_q_docs.append(sim_q_doc)

# Step 3: Pengukuran Kemiripan Semantik antara query dan dokumen
def calculate_semantic_similarity(sim_q_doc, document):    
    query_len = len(query) ** 2
    document_len = len(document) ** 2
    sim_sem = sim_q_doc 
    return abs(sim_sem)

sim_semantics_results = []
for i, sim in enumerate(sim_q_docs):
    sim_semantic = calculate_semantic_similarity(sim, documents[i]['preprocessed'])
    sim_semantics_results.append(sim_semantic)
    

# # Step 3: Menghitung Jaccard similarity
# def calculate_jaccard_similarity(query, document):
#     query_set = set(query)
#     document_set = set(document)
#     intersection = query_set.intersection(document_set)
#     union = query_set.union(document_set)
#     similarity = len(intersection) / len(union)
#     return similarity

# # Step 4: Menggabungkan cosine similarity dan Jaccard similarity
# def calculate_similarity(query, document):    
#     cosine_sim = calculate_cosine_similarity(query, document)   
#     jaccard_sim = calculate_jaccard_similarity(query, document)
#     similarity = (cosine_sim + jaccard_sim) / 2
#     return similarity

# # Step 5: Perhitungan kemiripan semantik
# similarities = []
# for i, doc_words in enumerate(document_words):
#     similarity = calculate_similarity(query_words, doc_words)
#     similarities.append(similarity)

# Step 6: Mengurutkan dokumen berdasarkan kemiripan tertinggi
sorted_documents = sorted(zip(documents, sim_semantics_results), key=lambda x: x[1], reverse=True)

for doc, similarity in sorted_documents:
    similarity_percentage = similarity * 100
    print(f"Similarity with document: {similarity}")
    print(f"Similarity percentage: {similarity_percentage:.3f}%")
    print(f"Preprocessed Document: {doc['preprocessed']}")
    print("------------")

# import os
# import compress_fasttext
# import numpy as np

# class WordEmbedding:
#     def __init__(self, model_path):
#         self.model = self.load_model(model_path)

#     def load_model(self, model_path):
#         current_directory = os.path.dirname(__file__)
#         pretrained_model_path = os.path.abspath(os.path.join(current_directory, model_path))
#         model = compress_fasttext.models.CompressedFastTextKeyedVectors.load(pretrained_model_path)
#         return model

#     def get_most_similar_words(self, words, topn=100):
#         word_vectors = self.model
#         similar_words = []
#         for word in words:
#             if word in word_vectors:
#                 similar = word_vectors.similar_by_word(word, topn=topn)
#                 similar_words.extend([word[0] for word in similar])
#         return similar_words

#     def calculate_cosine_similarity(self, query, document):    
#         query_vec = np.mean(self.model[query], axis=0)
#         document_vec = np.mean(self.model[document], axis=0)
#         similarities = self.model.cosine_similarities(query_vec, [document_vec])
#         similarity = similarities[0]
#         return similarity

# class JaccardSimilarity:
#     def calculate_similarity(self, query, document):
#         query_set = set(query)
#         document_set = set(document)
#         intersection = query_set.intersection(document_set)
#         union = query_set.union(document_set)
#         similarity = len(intersection) / len(union)
#         return similarity

# class SemanticSimilarity:
#     def __init__(self, word_embedding):
#         self.word_embedding = word_embedding

#     def calculate_similarity(self, query, document):    
#         cosine_sim = self.word_embedding.calculate_cosine_similarity(query, document)
#         jaccard_sim = JaccardSimilarity().calculate_similarity(query, document)
#         similarity = (cosine_sim + jaccard_sim) / 2
#         return similarity

#     def sort_documents(self, documents, similarities):
#         sorted_documents = sorted(zip(documents, similarities), key=lambda x: x[1], reverse=True)
#         return sorted_documents

# model_path = '../pretrained_model/cc.id.300.small.bin'
# word_embedding = WordEmbedding(model_path)

# jaccard_similarity = JaccardSimilarity()
# semantic_similarity = SemanticSimilarity(word_embedding)

# query = ['dengan', 'nama', 'allah', 'maha', 'asih', 'maha', 'sayang']

# documents = [
#     {'preprocessed': ['dengan', 'nama', 'allah', 'maha', 'asih', 'maha', 'sayang']},
#     {'preprocessed': ['puji', 'allah', 'tuhan', 'alam']},
#     {'preprocessed': ['maha', 'asih', 'maha', 'sayang']},
#     {'preprocessed': ['milik', 'hari', 'balas']},
#     {'preprocessed': ['engkau', 'kami', 'sembah', 'engkau', 'kami', 'tolong']},
#     {'preprocessed': ['tunjuk', 'kami', 'jalan', 'lurus']},
#     {'preprocessed': ['jalan', 'engkau', 'nikmat', 'kepada', 'jalan', 'mereka', 'murka', 'jalan', 'mereka', 'sesat']},
#     {'preprocessed': ['alif','lam', 'mim']}
# ]

# query_words = word_embedding.get_most_similar_words(query)
# document_words = [word_embedding.get_most_similar_words(doc['preprocessed']) for doc in documents]
# print(document_words[1])


# similarities = []
# for i, doc_words in enumerate(document_words):
#     similarity = semantic_similarity.calculate_similarity(query_words, doc_words)
#     similarities.append(similarity)

# sorted_documents = semantic_similarity.sort_documents(documents, similarities)

# for doc, similarity in sorted_documents:
#     similarity_percentage = similarity * 100
#     print(f"Similarity with document: {similarity}")
#     print(f"Similarity percentage: {similarity_percentage:.3f}%")
#     print(f"Preprocessed Document: {doc['preprocessed']}")
#     print("------------")
