import math
import sys
sys.path.append("src")

from preprocessing.preprocessing import Preprocessing
from database.database import get_all_ayahs


# Preprocessed query and documents
query = Preprocessing("Merekalah yang mendapat petunjuk dari Tuhannya, dan mereka itulah orang-orang yang beruntung.").execute()
documents = get_all_ayahs()

# Function to calculate term frequency (TF)
def calculate_tf(document : list, term : str):
    tf = document.count(term) / float(len(document))
    return tf

# Function to calculate inverse document frequency (IDF)
def calculate_idf(documents : list, term : str):
    num_documents_with_term = sum(1 for document in documents if term in document)
    if num_documents_with_term > 0:
        return 1.0 + math.log(float(len(documents) / (1 + num_documents_with_term)))
    else: 
        return 1.0

# Function to calculate TF-IDF
def calculate_tfidf(document : list, documents: list, term : str):
    tf = calculate_tf(document, term)
    idf = calculate_idf(documents, term)
    tfidf = tf * idf
    return tfidf

# Function to calculate cosine similarity
def calculate_cosine_similarity(query_vector : list, document_vector : list):
    dot_product = sum(x * y for x, y in zip(query_vector, document_vector))
    query_vector_length = math.sqrt(sum(x ** 2 for x in query_vector))
    document_vector_length = math.sqrt(sum(x ** 2 for x in document_vector))
    
    if query_vector_length == 0 or document_vector_length == 0:
        return 0  # Return zero similarity if either vector has zero length
    
    similarity = dot_product / (query_vector_length * document_vector_length)
    return similarity

# Calculate TF-IDF for query
query_tfidf = [calculate_tfidf(query, documents, term) for term in query]
# print(f"TF-IDF for query: {query_tfidf}")

# Calculate TF-IDF for each document and find cosine similarity
similarities = {}
for i, document in enumerate(documents):
    document_tfidf = [calculate_tfidf(document["preprocessed"], documents, term) for term in query]
    similarity = calculate_cosine_similarity(query_tfidf, document_tfidf)
    similarities[i] = similarity

# Sort the similarities in descending order
similarities = sorted(similarities.items(), key=lambda x: x[1], reverse=True)

# Print the top 10 similarity scores with percentages
for i, (document_index, similarity) in enumerate(similarities[:10]):
    similarity_percentage = similarity * 100
    print("surah id: ", documents[document_index]["surah_id"])
    print("ayah arabic: ", documents[document_index]["arabic"])
    print("ayah translation: ", documents[document_index]["translation"])
    print(f"Similarity score for document {document_index+1}: {similarity:.2f} : {similarity_percentage:.2f}%")
    print()
