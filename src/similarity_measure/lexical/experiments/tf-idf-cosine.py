import math

# Sample Documents
documents = [
    "I like to play football.",
    "Football is my favorite sport.",
    "I enjoy playing tennis.",
    "Tennis is a great sport.",
    "Basketball is fun to watch."
]

# Query
query = "I love football and tennis."

# Tokenize documents and query
def tokenize(text):
    return text.lower().split()

# Calculate TF (Term Frequency)
def calculate_tf(document):
    tf = {}
    tokens = tokenize(document)
    for token in tokens:
        tf[token] = tf.get(token, 0) + 1
    return tf

# Calculate IDF (Inverse Document Frequency)
def calculate_idf(documents):
    idf = {}
    total_documents = len(documents)
    for document in documents:
        tokens = set(tokenize(document))
        for token in tokens:
            idf[token] = idf.get(token, 0) + 1
    for token, count in idf.items():
        idf[token] = math.log10(total_documents / count)
    return idf

# Calculate TF-IDF
def calculate_tfidf(tf, idf):
    tfidf = {}
    for token, tf_value in tf.items():
        tfidf[token] = tf_value * idf.get(token, 0)
    return tfidf

# Calculate cosine similarity
def calculate_cosine_similarity(tfidf_query, tfidf_document):
    dot_product = sum(tfidf_query[token] * tfidf_document.get(token, 0) for token in tfidf_query)
    magnitude_query = math.sqrt(sum(tfidf_query[token] ** 2 for token in tfidf_query))
    magnitude_document = math.sqrt(sum(tfidf_document[token] ** 2 for token in tfidf_document))
    if magnitude_query == 0 or magnitude_document == 0:
        return 0
    return dot_product / (magnitude_query * magnitude_document)

# Tokenize and calculate TF-IDF for documents
tf_documents = []
for document in documents:
    tf_documents.append(calculate_tf(document))
idf = calculate_idf(documents)
tfidf_documents = []
for tf in tf_documents:
    tfidf_documents.append(calculate_tfidf(tf, idf))

# Tokenize and calculate TF-IDF for the query
query_tf = calculate_tf(query)
tfidf_query = calculate_tfidf(query_tf, idf)

# Calculate cosine similarity between the query and documents
cosine_similarities = []
for tfidf_document in tfidf_documents:
    cosine_similarities.append(calculate_cosine_similarity(tfidf_query, tfidf_document))

# Sort documents by cosine similarity (in descending order)
sorted_documents = sorted(zip(documents, cosine_similarities), key=lambda x: x[1], reverse=True)

# Print the sorted documents
for document, cosine_similarity in sorted_documents:
    print(f"Document: {document}")
    print(f"Cosine Similarity: {cosine_similarity}")
    print()
