# import numpy as np

# class CosineSimilarity:
#     def __init__(self, documents, tfidf_dict_qry, df, query):
#         self.documents = documents
#         self.tfidf_dict_qry = tfidf_dict_qry
#         self.df = df
#         self.query = query
        
#     def compute(self, df, doc_num):
#         dot_product = 0
#         qry_mod = 0
#         doc_mod = 0

#         for keyword in self.query:
#             dot_product += self.tfidf_dict_qry[keyword] * df[keyword][df['doc'] == doc_num]
#             qry_mod += self.tfidf_dict_qry[keyword] * self.tfidf_dict_qry[keyword]
#             doc_mod += df[keyword][df['doc'] == doc_num] * df[keyword][df['doc'] == doc_num]
#         qry_mod = np.sqrt(qry_mod)
#         doc_mod = np.sqrt(doc_mod)
#         denominator = qry_mod * doc_mod
#         cos_sim = dot_product / denominator

#         return cos_sim
    
#     def rank_similarity_docs(self):
#         cos_sim = []
#         for doc_num in range(0, len(self.documents)):
#             cos_sim.append(self.compute( self.df, doc_num).tolist())
#         return cos_sim
import numpy as np

# class CosineSimilarity:
#     def __init__(self, documents, tfidf_dict_qry, df, query):
#         self.documents = documents
#         self.tfidf_dict_qry = tfidf_dict_qry
#         self.df = df
#         self.query = query
        
#     def compute(self, df, doc_num):
#         dot_product = 0
#         qry_mod = 0
#         doc_mod = 0

#         for keyword in self.query:
#             dot_product += self.tfidf_dict_qry[keyword] * df.loc[df['doc'] == doc_num, keyword].values[0]
#             qry_mod += self.tfidf_dict_qry[keyword] ** 2
#             doc_mod += df.loc[df['doc'] == doc_num, keyword].values[0] ** 2
        
#         qry_mod = np.sqrt(qry_mod)
#         doc_mod = np.sqrt(doc_mod)
#         denominator = qry_mod * doc_mod

#         # Handle division by zero
#         if np.any(denominator != 0) and not np.isnan(denominator).any():
#             cos_sim = dot_product / denominator
#         else:
#             cos_sim = 0.0

#         return cos_sim
    
#     def rank_similarity_docs(self):
#         cos_sim = []
#         for doc_num in range(0, len(self.documents)):
#             cos_sim.append(self.compute(self.df, doc_num["preprocessed"]))
#         return cos_sim

class CosineSimilarity:
    @staticmethod
    def compute(tfidf_dict_qry, df, query, doc_num):
        dot_product = 0
        qry_mod = 0
        doc_mod = 0
    
        for keyword in query:
            dot_product += tfidf_dict_qry[keyword] * df[keyword][df['doc'] == doc_num]
            qry_mod += tfidf_dict_qry[keyword] * tfidf_dict_qry[keyword]
            doc_mod += df[keyword][df['doc'] == doc_num] * df[keyword][df['doc'] == doc_num]
        qry_mod = np.sqrt(qry_mod)
        doc_mod = np.sqrt(doc_mod)
        denominator = qry_mod * doc_mod
        cos_sim = dot_product / denominator

        return cos_sim


class RankSimilarityDocs:
    def __init__(self, documents, tfidf_dict_qry, df, query):
        self.documents = documents
        self.tfidf_dict_qry = tfidf_dict_qry
        self.df = df
        self.query = query

    def compute(self):
        cos_sim = []
        for doc_num in range(0, len(self.documents)):
            cos_sim.append(CosineSimilarity.compute(self.tfidf_dict_qry, self.df, self.query, doc_num).tolist())
        return cos_sim
