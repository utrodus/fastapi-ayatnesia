# import sys
# import os
# sys.path.append("src")
# import compress_fasttext
# import numpy as np

# current_directory = os.path.dirname(__file__)

# small_pretrained_model_path = os.path.abspath(os.path.join(current_directory, '../pretrained_model/cc.id.300.small.bin'))

# model = compress_fasttext.models.CompressedFastTextKeyedVectors.load(small_pretrained_model_path)
# # print(model.similarity('maksud', 'maksud'))

# def calculate_semantic_similarity(query, documents):
#     similarities = []
#     for document in documents:
#         document_words = document['preprocessed']
#         document_embedding = np.mean([model[word] for word in document_words if word in model], axis=0)
#         query_embedding = np.mean([model[word] for word in query if word in model], axis=0)
#         similarity = np.dot(query_embedding, document_embedding) / (np.linalg.norm(query_embedding) * np.linalg.norm(document_embedding))
#         similarities.append(similarity)

#     # Calculate Jaccard similarity
#     jaccard_similarities = [similarity / (2 - similarity) for similarity in similarities]

#     # Sort documents based on similarity score
#     sorted_documents = sorted(zip(documents, jaccard_similarities), key=lambda x: x[1], reverse=True)

#     return sorted_documents

# # Test the code with the given query and documents
# query = ['allah', 'perkasa', 'seluruh', 'luas']
# documents = [
#     {"preprocessed": ["dengan", "nama", "allah", "maha", "asih", "maha", "sayang"]},
#     {"preprocessed": ["puji", "allah", "tuhan", "alam"]},
#     {"preprocessed": ["milik","hari","balas"]},
#     {"preprocessed": ["maha", "besar", "allah", "tuhan", "semesta", "alam"]},
#     {"preprocessed": ["tunjuk","kami","jalan","lurus"]},  
# ]

# results = calculate_semantic_similarity(query, documents)

# # Display the similarity scores and sorted documents
# for document, similarity in results:
#     print(f"Similarity Score: {similarity}")
#     print("Document:", document)
#     print()

import os
import compress_fasttext
import numpy as np

class SemanticSimilarityCalculator:
    def __init__(self, pretrained_model_path):
        self.model = compress_fasttext.models.CompressedFastTextKeyedVectors.load(pretrained_model_path)

    def word_embedding(self, words):
        embeddings = [self.model[word] for word in words if word in self.model]
        return np.mean(embeddings, axis=0) if embeddings else None

    def calculate_cosine_similarity(self, vector1, vector2):
        dot_product = np.dot(vector1, vector2)
        norm_product = np.linalg.norm(vector1) * np.linalg.norm(vector2)
        return dot_product / norm_product

    def calculate_jaccard_similarity(self, similarity):
        return similarity / (2 - similarity)

    def sort_documents(self, documents, similarities):
        return sorted(zip(documents, similarities), key=lambda x: x[1], reverse=True)

    def calculate_similarity(self, query, documents):
        similarities = []
        for document in documents:
            document_embedding = self.word_embedding(document['preprocessed'])
            query_embedding = self.word_embedding(query)
            if document_embedding is not None and query_embedding is not None:
                similarity = self.calculate_cosine_similarity(query_embedding, document_embedding)
                similarities.append(similarity)
        jaccard_similarities = [self.calculate_jaccard_similarity(similarity) for similarity in similarities]
        combined_similarities = [a * b for a, b in zip(similarities, jaccard_similarities)]
        return self.sort_documents(documents, combined_similarities)


# Test the code with the given query and documents
current_directory = os.path.dirname(__file__)
small_pretrained_model_path = os.path.abspath(os.path.join(current_directory, '../pretrained_model/cc.id.300.small.bin'))

query = ['memohon','beri','pilih', 'rute', 'lintasan', 'tegak', 'terbuka', 'baik']
documents = [
 {'preprocessed': ['dengan', 'nama', 'allah', 'maha', 'asih', 'maha', 'sayang']}, 
 {'preprocessed': ['puji', 'allah', 'tuhan', 'alam']}, 
 {'preprocessed': ['maha', 'asih', 'maha', 'sayang']},
 {'preprocessed': ['milik', 'hari', 'balas']}, 
 {'preprocessed': ['engkau', 'kami', 'sembah', 'engkau', 'kami', 'tolong']}, 
 {'preprocessed': ['tunjuk', 'kami', 'jalan', 'lurus']},
 {'preprocessed': ['jalan', 'engkau', 'nikmat', 'kepada', 'jalan', 'mereka', 'murka', 'jalan', 'mereka', 'sesat']}
]

calculator = SemanticSimilarityCalculator(small_pretrained_model_path)
results = calculator.calculate_similarity(query, documents)

# Display the similarity scores and sorted documents
for document, similarity in results:
    print(f"Similarity Score: {similarity}")
    print("Document:", document)
    print()
