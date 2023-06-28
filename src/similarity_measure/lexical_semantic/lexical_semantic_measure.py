import sys
sys.path.append("src")
from database.database import get_surah_name_by_id
from similarity_measure.lexical.lexical_measure import LexicalMeasure
from similarity_measure.semantic.semantic_measure import SemanticMeasure

class LexicalSemanticMeasure:
    def __init__(self, all_ayahs:list, lexical_measure : LexicalMeasure, semantic_measure: SemanticMeasure):
        self.all_ayahs = all_ayahs
        self.lexical_measure = lexical_measure
        self.semantic_measure = semantic_measure
        self.alpha = 0.5
    
    def measure_lexical_similarity(self, query : list):
        lexical_measure_results = self.lexical_measure.calculate_lexical_similarity(query)
        lexical_measure_results = sorted(lexical_measure_results, key=lambda x: x['similarity'], reverse=False)
        return lexical_measure_results
    
    def measure_semantic_similarity(self, query : list):
        semantic_measure_results = self.semantic_measure.calculate_semantic_similarity(query)
        semantic_measure_results = sorted(semantic_measure_results, key=lambda x: x['similarity'], reverse=False)
        return semantic_measure_results
        
    def calculate_lexical_semantic_similarity(self, query : list):
        results = []
        lexical_similarity_results = self.measure_lexical_similarity(query)
        semantic_measure_results = self.measure_semantic_similarity(query)
        for i, ayah in enumerate(lexical_similarity_results):       
            combined_similarity = (lexical_similarity_results[i]['similarity'] + semantic_measure_results[i]['similarity']) / 2
            result = {
                'surah_id': ayah['surah_id'],
                'surat_name': get_surah_name_by_id(ayah['surah_id']),
                'similarity': float(combined_similarity),
                'arabic': ayah['arabic'],
                'translation': ayah['translation'],
                'numberInQuran': ayah['numberInQuran'],
                'numberInSurah': ayah['numberInSurah'],
                'tafsir': ayah['tafsir']
            }
            results.append(result)
        results = sorted(results, key=lambda x: x['similarity'], reverse=True)                 
        return results
    
    def get_top_similarities(self, query:list, top_relevance):
        results = self.calculate_lexical_semantic_similarity(query)
        if top_relevance == "all":
            top_results = [result for result in results if result['similarity'] > 0]
            top_results = results
        else: 
            top_relevance = int(top_relevance)
            results = results[:top_relevance]
            results = [result for result in results if result['similarity'] > 0]                   
            top_results = results 
        return top_results     
                        
        
# example usage
# all_ayahs = get_all_ayahs()
# lexical_semantic_measure = LexicalSemanticMeasure(all_ayahs)
# query = ['istimewa', 'hewan', 'ternak', 'alquran']
# top_results = lexical_semantic_measure.get_top_similarities(query, 10)
# for i in top_results:
#     print(i['surat_name'], i['arabic'], i['translation'], i['tafsir'],i['similarity'])
                