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

import sys
import os
sys.path.append("src")
import compress_fasttext
import numpy as np

class SemanticSimilarityCalculator:
    def __init__(self, pretrained_model_path):
        self.model = compress_fasttext.models.CompressedFastTextKeyedVectors.load(pretrained_model_path)

    def calculate_cosine_similarity(self, vector1, vector2):
        dot_product = np.dot(vector1, vector2)
        norm_product = np.linalg.norm(vector1) * np.linalg.norm(vector2)
        similarity = dot_product / norm_product
        return similarity

    def calculate_jaccard_similarity(self, similarity):
        jaccard_similarity = similarity / (2 - similarity)
        return jaccard_similarity

    def calculate_similarity(self, query, documents):
        similarities = []
        for document in documents:
            document_words = document['preprocessed']
            document_embedding = np.mean([self.model[word] for word in document_words if word in self.model], axis=0)
            query_embedding = np.mean([self.model[word] for word in query if word in self.model], axis=0)
            similarity = self.calculate_cosine_similarity(query_embedding, document_embedding)
            similarities.append(similarity)

        jaccard_similarities = [self.calculate_jaccard_similarity(similarity) for similarity in similarities]

        sorted_documents = sorted(zip(documents, jaccard_similarities), key=lambda x: x[1], reverse=True)

        return sorted_documents


# Test the code with the given query and documents
current_directory = os.path.dirname(__file__)
small_pretrained_model_path = os.path.abspath(os.path.join(current_directory, '../pretrained_model/cc.id.300.small.bin'))

query = ['allah', 'perkasa', 'seluruh', 'luas']
documents = [
    {"preprocessed": ["dengan", "nama", "allah", "maha", "asih", "maha", "sayang"]},
    {"preprocessed": ["puji", "allah", "tuhan", "alam"]},
    {"preprocessed": ["milik","hari","balas"]},
    {"preprocessed": ["maha", "besar", "allah", "tuhan", "semesta", "alam"]},
    {"preprocessed": ["tunjuk","kami","jalan","lurus"]},  
]

calculator = SemanticSimilarityCalculator(small_pretrained_model_path)
results = calculator.calculate_similarity(query, documents)

# Display the similarity scores and sorted documents
for document, similarity in results:
    print(f"Similarity Score: {similarity}")
    print("Document:", document)
    print()
