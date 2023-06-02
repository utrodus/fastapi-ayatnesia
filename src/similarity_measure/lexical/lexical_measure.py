import sys
sys.path.append("src")
from preprocessing.preprocessing import Preprocessing
from database.database import get_all_ayahs
from tf_idf import TFIDF
from cosine_similarity import RankSimilarityDocs

class LexicalMeasure:
    def __init__(self, query):
        self.query = Preprocessing(query).execute()
        self.documents = get_all_ayahs()        
    
    def execute(self):
        tfidf = TFIDF(self.documents)        
        # compute tf-idf for query
        self.query_norm_tf = tfidf.compute_query_tf(self.query)
        self.idf_dict_qry = tfidf.compute_query_idf(self.query)                
        tfidf_dict_qry = tfidf.compute_query_tfidf(self.query)        
        
        # # compute tf-idf for documents
        self.tf_doc = tfidf.tf_doc
        # print(self.tf_doc)
        self.idf_dict = tfidf.idf_dict
        # print(self.idf_dict)
        self.tf_idf, self.df = tfidf.compute_tfidf_with_alldocs(self.query)
        # print(self.df)
        
        # compute cosine similarity for find similarity between query and documents and rank them
        rank_documents = RankSimilarityDocs(self.documents, tfidf_dict_qry, self.df, self.query).compute()
        print(list(rank_documents))

lexical_measure = LexicalMeasure("Dengan nama Allah yang maha pengasih lagi maha penyayang").execute()
