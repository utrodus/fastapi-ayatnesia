import numpy as np
import math
import pandas as pd
# from db_helper import get_all_ayahs
from preprocessing.preprocessing import Preprocessing
# #all ayahs docs
# all_ayah_docs = get_all_ayahs()

class LexicalMeasure:
    def __init__(self, documents, query):
        self.query = query
        self.all_ayah_docs = documents
    
    def termFrequency(self, term, document):      
        return document.count(term) / float(len(document))
    
    def compute_normalizedtf_all_ayah_docs(self):
        tf_doc = []
        for txt in self.all_ayah_docs:
            sentence = txt['preprocessed']
            norm_tf= dict.fromkeys(set(sentence), 0)
            for word in sentence:
                norm_tf[word] = self.termFrequency(word, sentence)
            tf_doc.append(norm_tf)    
        self.tf_doc = tf_doc
    
    def inverseDocumentFrequency(self, term):
        numDocumentsWithThisTerm = 0        
        for doc in range (0, len(self.all_ayah_docs)):
            if term in self.all_ayah_docs[doc]['preprocessed']:
                numDocumentsWithThisTerm = numDocumentsWithThisTerm + 1
        if numDocumentsWithThisTerm > 0:
            return 1.0 + math.log(float(len(self.all_ayah_docs)) / numDocumentsWithThisTerm)
        else:
            return 1.0
        
    def compute_idf_all_ayah_docs(self):
        idf_dict = {}
        for doc in self.all_ayah_docs:        
            for word in doc['preprocessed']:
                idf_dict[word] = self.inverseDocumentFrequency(word)
        self.idf_dict = idf_dict
    
    # tf-idf score across all docs for the query string("life learning")
    def compute_tfidf_all_ayah_docs(self):
        tf_idf = []
        index = 0
        query_tokens = self.query
        df = pd.DataFrame(columns=['doc'] + query_tokens)
        for doc in self.all_ayah_docs:
            df['doc'] = np.arange(0 , len(self.all_ayah_docs))
            doc_num = self.tf_doc[index]
            sentence = doc['preprocessed']
            for word in sentence:
                for text in query_tokens:
                    if(text == word):                 
                        tf_idf_score = doc_num[word] * self.idf_dict[word]
                        tf_idf.append(tf_idf_score)
                        df.iloc[index, df.columns.get_loc(word)] = tf_idf_score
            index += 1
        df.fillna(0 , axis=1, inplace=True)
        self.df = df
        self.tf_idf = tf_idf
        return tf_idf , df
    
    def compute_tf_query(self):
        query_norm_tf = {}
        for word in self.query:
            query_norm_tf[word] = self.termFrequency(word, self.query)
        self.query_norm_tf = query_norm_tf            
    
    def compute_idf_query(self):
        idf_dict_qry = {}
        sentence = self.query
        for word in sentence:
            idf_dict_qry[word] = self.inverseDocumentFrequency(word)
        self.idf_dict_qry = idf_dict_qry            
    
    def compute_tfidf_query(self):
        tfidf_dict_qry = {}
        sentence = self.query
        for word in sentence:
            tfidf_dict_qry[word] = self.query_norm_tf[word] * self.idf_dict_qry[word]
        self.tfidf_dict_qry = tfidf_dict_qry
        
    def cosine_similarity(self, doc_num):
        dot_product = 0
        qry_mod = 0
        doc_mod = 0
        tokens = query
    
        for keyword in tokens:
            dot_product += self.tfidf_dict_qry[keyword] * self.df[keyword][self.df['doc'] == doc_num]
            #||Query||
            qry_mod += self.tfidf_dict_qry[keyword] * self.tfidf_dict_qry[keyword]
            #||Document||
            doc_mod += self.df[keyword][self.df['doc'] == doc_num] * self.df[keyword][self.df['doc'] == doc_num]
        qry_mod = np.sqrt(qry_mod)
        doc_mod = np.sqrt(doc_mod)
        #implement formula
        denominator = qry_mod * doc_mod
        cos_sim = dot_product/denominator
        
        return cos_sim
    
    def rank_similarity_docs(self):
        cos_sim =[]
        for doc_num in range(0 , len(self.all_ayah_docs)):
            cos_sim.append(self.cosine_similarity(doc_num).tolist())
        return cos_sim    
    
    def execute(self):
        self.compute_normalizedtf_all_ayah_docs()
        self.compute_idf_all_ayah_docs()        
        result = self.compute_tfidf_all_ayah_docs()
        return result
        # self.compute_tf_query()
        # self.compute_idf_query()
        # self.compute_tfidf_query()
        # rank_similarity = self.rank_similarity_docs()
        # return rank_similarity
       
        
        
        
    
query = "Dengan nama Allah Yang Maha Pengasih, Maha Penyayang."
query_preprocessed = Preprocessing(query).execute()
documents = get_all_ayahs()
lexical_measure_result = LexicalMeasure(documents, query_preprocessed).execute()    
print(lexical_measure_result)      