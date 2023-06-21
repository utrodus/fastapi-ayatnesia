import sys
sys.path.append("src")
from database.database import get_all_ayahs, get_surah_name_by_id
from similarity_measure.semantic.word_embedding import WordEmbedding

class SemanticMeasure:
    def __init__(self):              
        self.word_embedding = WordEmbedding()        
        self.all_ayahs = get_all_ayahs()

    def sort_documents(self):
        self.results = sorted(self.results, key=lambda x: x[1], reverse=True)

    def calculate_semantic_similarity(self, query):
        results = []
        query_vector = self.word_embedding.get_words_vector(query)
        for ayah in self.all_ayahs:
            ayah_vector = self.word_embedding.get_words_vector(ayah['preprocessed'])
            similarity = self.word_embedding.calculate_similarity(query_vector, ayah_vector)
            result = {
                'id': ayah['id'],
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
    
    def get_top_similarities(self, query, top_relevance):
        results = self.calculate_semantic_similarity(query)
        if top_relevance == "all":
            top_results = results
        else: 
            top_relevance = int(top_relevance)                   
            top_results = results[:top_relevance]
        return top_results                    

# example usage    
# semantic_measure = SemanticMeasure()
# query = ['istimewa', 'hewan', 'ternak', 'alquran']
# top_results = semantic_measure.get_top_similarities(query)    
# for i in top_results:
#     print(i['surat_name'], i['arabic'], i['translation'], i['tafsir'],i['similarity'])
