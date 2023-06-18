import sys
sys.path.append("src")
from database.database import get_all_ayahs, get_surah_name_by_id
from similarity_measure.semantic.word_embedding import WordEmbedding
from similarity_measure.semantic.jaccard_similarity import JaccardSimilarity

class SemanticMeasure:
    def __init__(self):
        self.documents = get_all_ayahs()
        self.results = []
        self.similarities = {}
        self.nearest_ayahs_words = []
        self.word_embedding = WordEmbedding()
        self.get_doc_nearest_words()
        # self.w_cosine = 0.7 # Bobot untuk cosine similarity
        # self.w_jaccard = 0.3 # Bobot untuk Jaccard similarity

    def sort_documents(self):
        self.similarities = sorted(self.similarities.items(), key=lambda x: x[1], reverse=True)

    def get_query_nearest_words(self, query):
        self.nearest_query_words = self.word_embedding.get_nearest_words(query)

    def get_doc_nearest_words(self):
        for doc in self.documents:
            self.nearest_ayahs_words.append(doc['word_embedding_result'])

    def calculate_semantic_similarity(self, query):
        self.get_query_nearest_words(query)
        query_and_doc_similarity = [self.word_embedding.calculate_similarity(self.nearest_query_words, doc_words) for doc_words in self.nearest_ayahs_words]
        jaccard_similarity = [JaccardSimilarity().calculate(self.nearest_query_words, doc_words) for doc_words in self.nearest_ayahs_words]
        for i in range(len(self.documents)):            
            self.similarities[i] = (query_and_doc_similarity[i] + jaccard_similarity[i]) / 2
            # (self.w_cosine * query_and_doc_similarity[i] + self.w_jaccard * jaccard_similarity[i]) 
            # / (self.w_cosine + self.w_jaccard)
                    
        return self.similarities
    
    def get_top_similarities(self, top_relevance):
        self.sort_documents()
        self.results = []
        def transform_similarity(document_index, similarity):
            similarity_percentage = similarity * 100
            return {
                "surah_id": self.documents[document_index]["surah_id"],
                "surah_name": get_surah_name_by_id(self.documents[document_index]["surah_id"]),
                "ayah_arabic": self.documents[document_index]["arabic"],
                "ayah_translation": self.documents[document_index]["translation"],
                "number_in_surah": self.documents[document_index]['number']['inSurah'],
                "tafsir": self.documents[document_index]["tafsir"],
                "similarity_score": f"{similarity:.4f}",
                "similarity_percentage": f"{similarity_percentage:.2f}%",
            }

        if top_relevance == "all":
            self.results = list(
                map(transform_similarity, *zip(*self.similarities))
            )
        else:
            top_relevance = int(top_relevance)
            self.results = list(
                map(transform_similarity, *zip(*self.similarities[:top_relevance]))
            )
                        
        return self.results

# query = "Dengan Menyebut Nama Allah Yang Maha Pengasih Lagi Maha Penyayang"
# query_preprocessed = Preprocessing(query).execute()
# semantic_measure = SemanticMeasure()
# semantic_measure.calculate_semantic_similarity(query_preprocessed)
# results = semantic_measure.get_top_similarities()
# for result in results:
#     print(result)
            