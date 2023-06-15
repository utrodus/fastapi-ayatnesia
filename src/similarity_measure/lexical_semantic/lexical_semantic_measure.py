import sys
sys.path.append("src")
from database.database import get_all_ayahs, get_surah_name_by_id
from similarity_measure.lexical.lexical_measure import LexicalMeasure
from similarity_measure.semantic.semantic_measure import SemanticMeasure

class LexicalSemanticMeasure:
    def __init__(self):
        self.documents = get_all_ayahs()
        self.lexical_measure = LexicalMeasure()
        self.semantic_measure = SemanticMeasure()
        self.combined_similarity = {}
        self.results = []
    
    def measure_lexical_similarity(self, query : list):
        return self.lexical_measure.calculate_lexical_similarity(query)
    
    def measure_semantic_similarity(self, query : list):
        return self.semantic_measure.calculate_semantic_similarity(query)
    
    # sort similarities in descending order
    def sort_similarities(self):
        self.combined_similarity = sorted(self.combined_similarity.items(), key=lambda x: x[1], reverse=True)
        
    def calculate_lexical_semantic_similarity(self, query : list):
        lexical_similarity = self.measure_lexical_similarity(query)
        semantic_similarity = self.measure_semantic_similarity(query)
        
        for i in range(len(self.documents)):
            self.combined_similarity[i] = (lexical_similarity[i] + semantic_similarity[i]) / 2
    
    def get_top_similarities(self, limit = 5):
        self.sort_similarities()        
        for i, (document_index, similarity) in enumerate(self.combined_similarity[:limit]):
            similarity_percentage = similarity * 100
            self.results.append({
                "surah_id": self.documents[document_index]["surah_id"],
                "surah_name": get_surah_name_by_id(self.documents[document_index]["surah_id"]),
                "ayah_arabic": self.documents[document_index]["arabic"],
                "ayah_translation": self.documents[document_index]["translation"],
                "number_in_surah": self.documents[document_index]['number']['inSurah'],
                "tafsir": self.documents[document_index]["tafsir"],
                "similarity_score": f"{similarity:.4f}",
                "similarity_percentage": f"{similarity_percentage:.2f}%",
            })
        return self.results 
                        
    
    
# query = "Dengan Menyebut Nama Allah Yang Maha Pengasih Lagi Maha Penyayang"
# query_preprocessed = Preprocessing(query).execute()
# lexical_semantic_measure = LexicalSemanticMeasure()
# lexical_semantic_measure.calculate_lexical_semantic_similarity(query_preprocessed)
# results = lexical_semantic_measure.get_top_similarities()
# for result in results:
#     print(result)
                