import sys
sys.path.append("src")
from database.database import get_all_ayahs
from similarity_measure.lexical.tf_idf import TFIDF
from similarity_measure.lexical.cosine_similarity import CosineSimilarity

class LexicalMeasure:
    # initialize documents, results, and similarities
    def __init__(self):
        self.documents = get_all_ayahs()
        self.results = []
        self.similarities = {}      
          
    # Clear results and similarities 
    def clear_results(self):
        self.results.clear() 
        self.similarities.clear()
        
    # Calculate TF-IDF for each document and find cosine similarity
    def calculate_lexical_similarity(self, query : list):
        self.clear_results()
        query_tfidf = [TFIDF.calculate(query, self.documents, term) for term in query]
        
        for i, document in enumerate(self.documents):
            document_tfidf = [TFIDF.calculate(document["preprocessed"], self.documents, term) for term in query]
            similarity = CosineSimilarity.calculate(query_tfidf, document_tfidf)
            self.similarities[i] = similarity
                        
        self.sort_similarities()
    
    # sort similarities in descending order
    def sort_similarities(self):
        self.similarities = sorted(self.similarities.items(), key=lambda x: x[1], reverse=True)
        
    # get top similarities with limit = 5 (default), limit is the number of top similarities
    def get_top_similarities(self, limit = 5):
        for i, (document_index, similarity) in enumerate(self.similarities[:limit]):
            similarity_percentage = similarity * 100
            self.results.append({
                "surah_id": self.documents[document_index]["surah_id"],
                "ayah_arabic": self.documents[document_index]["arabic"],
                "ayah_translation": self.documents[document_index]["translation"],
                "number_in_surah": self.documents[document_index]['number']['inSurah'],
                "tafsir": self.documents[document_index]["tafsir"],
                "similarity_score": f"{similarity:.4f}",
                "similarity_percentage": f"{similarity_percentage:.2f}%",
            })
        return self.results         