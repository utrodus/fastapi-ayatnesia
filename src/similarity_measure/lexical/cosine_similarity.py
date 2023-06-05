import math

class CosineSimilarity:
    @staticmethod
    # Function to calculate cosine similarity
    def calculate(query_vector : list, document_vector : list):
        dot_product = sum(x * y for x, y in zip(query_vector, document_vector))
        query_vector_length = math.sqrt(sum(x ** 2 for x in query_vector))
        document_vector_length = math.sqrt(sum(x ** 2 for x in document_vector))
        
        if query_vector_length == 0 or document_vector_length == 0:
            return 0  # Return zero similarity if either vector has zero length
        
        similarity = dot_product / (query_vector_length * document_vector_length)
        return similarity