import sys
sys.path.append("src")
from database.database import get_surah_name_by_id
from similarity_measure.semantic.word_embedding import WordEmbedding

class SemanticMeasure:
    def __init__(self, word_embedding:WordEmbedding, all_ayahs:list):              
        self.word_embedding = word_embedding        
        self.all_ayahs = all_ayahs

    def calculate_semantic_similarity(self, query:list):
        results = []
        query_vector = self.word_embedding.get_words_vector(query)
        for ayah in self.all_ayahs:
            ayah_vector = self.word_embedding.get_words_vector(ayah['preprocessed'])
            similarity = self.word_embedding.calculate_similarity(query_vector, ayah_vector)
            result = {
                'surah_id': ayah['surah_id'],
                'surat_name': get_surah_name_by_id(ayah['surah_id']),
                'similarity': float(similarity),
                'similarity_percentage': round(float(similarity) * 100, 2),
                'arabic': ayah['arabic'],
                'translation': ayah['translation'],
                'numberInQuran': ayah['number']['inQuran'],
                'numberInSurah': ayah['number']['inSurah'],
                'tafsir': ayah['tafsir']
            }
            results.append(result)
        results = sorted(results, key=lambda x: x['similarity'], reverse=True)            
        return results
    
    def get_top_similarities(self, query:list, top_relevance):
        results = self.calculate_semantic_similarity(query)
        if top_relevance == "all":
            top_results = [result for result in results if result['similarity'] > 0.6]
        else:
            top_relevance = int(top_relevance)
            results = results[:top_relevance]
            results = [result for result in results if result['similarity'] > 0]                   
            top_results = results 
        return top_results                    

# example usage    
# semantic_measure = SemanticMeasure()
# query = ['istimewa', 'hewan', 'ternak', 'alquran']
# top_results = semantic_measure.get_top_similarities(query, 10)    
# for i in top_results:
#     print(i['surat_name'], i['arabic'], i['translation'], i['tafsir'],i['similarity'])
