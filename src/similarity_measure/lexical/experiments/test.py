import math

# Function to calculate term frequency (TF)
def calculate_tf(document, term):
    tf = document.count(term)
    return tf

# Function to calculate inverse document frequency (IDF)
def calculate_idf(documents, term):
    num_documents_with_term = sum(1 for document in documents if term in document)
    idf = math.log(len(documents) / (1 + num_documents_with_term))
    return idf

# Function to calculate TF-IDF
def calculate_tfidf(document, documents, term):
    tf = calculate_tf(document, term)
    idf = calculate_idf(documents, term)
    tfidf = tf * idf
    return tfidf

# Function to calculate cosine similarity
def calculate_cosine_similarity(query_vector, document_vector):
    dot_product = sum(x * y for x, y in zip(query_vector, document_vector))
    query_vector_length = math.sqrt(sum(x ** 2 for x in query_vector))
    document_vector_length = math.sqrt(sum(x ** 2 for x in document_vector))
    
    if query_vector_length == 0 or document_vector_length == 0:
        return 0  # Return zero similarity if either vector has zero length
    
    similarity = dot_product / (query_vector_length * document_vector_length)
    return similarity

# Preprocessed query and documents
query = ["allah", "maha", "asih"]
documents = [
    {"preprocessed": ["dengan", "nama", "allah", "maha", "asih", "maha", "sayang"]},
    {"preprocessed": ["puji", "allah", "tuhan", "alam"]},
    {"preprocessed": ["milik","hari","balas"]},
    {"preprocessed": ["maha", "besar", "allah", "tuhan", "semesta", "alam"]}  
]

# Calculate TF-IDF for query
query_tfidf = [calculate_tfidf(query, documents, term) for term in query]

# Calculate TF-IDF for each document and find cosine similarity
similarities = []
for document in documents:
    document_tfidf = [calculate_tfidf(document["preprocessed"], documents, term) for term in query]
    similarity = calculate_cosine_similarity(query_tfidf, document_tfidf)
    similarities.append(similarity)

# Print the similarity scores
for i, similarity in enumerate(similarities):
    print(f"Similarity score for document {i+1}: {similarity}")
