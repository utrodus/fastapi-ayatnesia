import sys
sys.path.append("src")
from database.database import get_surah_name_by_id
from similarity_measure.lexical.tf_idf import TFIDF
from similarity_measure.lexical.cosine_similarity import CosineSimilarity

class LexicalMeasure:
    # initialize documents, results, and similarities
    def __init__(self, all_ayahs:list):
        self.all_ayahs = all_ayahs

    # Calculate TF-IDF for each document and find cosine similarity
    def calculate_lexical_similarity(self, query : list):
        results = []
        query_tfidf = [TFIDF.calculate(query, self.all_ayahs, term) for term in query]
        
        for ayah in self.all_ayahs:
            document_tfidf = [TFIDF.calculate(ayah["preprocessed"], self.all_ayahs, term) for term in query]
            similarity = CosineSimilarity.calculate(query_tfidf, document_tfidf)
            result = {
                'surah_id': ayah['surah_id'],
                'surat_name': get_surah_name_by_id(ayah['surah_id']),
                'similarity': float(similarity),
                'arabic': ayah['arabic'],
                'translation': ayah['translation'],
                'numberInQuran': ayah['number']['inQuran'],
                'numberInSurah': ayah['number']['inSurah'],
                'tafsir': ayah['tafsir']
            }
            results.append(result)
        results = sorted(results, key=lambda x: x['similarity'], reverse=True)   
        return results
        
    # get top similarities with limit = 5 (default), limit is the number of top similarities
    def get_top_similarities(self, query, top_relevance):
        results = self.calculate_lexical_similarity(query)
        if top_relevance == "all":
            top_results = results
        else: 
            top_relevance = int(top_relevance)                   
            top_results = results[:top_relevance]
        return top_results             
    
# example usage
# all_ayahs = get_all_ayahs()
# lexical_measure = LexicalMeasure(all_ayahs)
# query = ['istimewa', 'hewan', 'ternak', 'alquran']
# top_results = lexical_measure.get_top_similarities(query, 10)
# for i in top_results:
#   print(i['surat_name'], i['arabic'], i['translation'], i['tafsir'],i['similarity'])