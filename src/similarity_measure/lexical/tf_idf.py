import numpy as np
import math
import pandas as pd

class TFIDF:
    def __init__(self, documents):
        self.documents = documents
        self.tf_doc = self.compute_normalized_tf(documents)
        self.idf_dict = self.compute_idf(documents)
        self.query_norm_tf = {}
        self.idf_dict_qry = {}
        self.tfidf_dict_qry = {}
        self.df = None

    @staticmethod
    def term_frequency(term, document):
        return document.count(term) / float(len(document))

    def compute_normalized_tf(self, documents):
        tf_doc = []
        for doc in documents:
            preprocessed_doc = doc["preprocessed"]
            norm_tf = dict.fromkeys(set(preprocessed_doc), 0)
            for word in preprocessed_doc:
                norm_tf[word] = self.term_frequency(word, preprocessed_doc)
            tf_doc.append(norm_tf)
            df = pd.DataFrame([norm_tf])
            idx = 0
            new_col = ["Normalized TF"]
            df.insert(loc=idx, column='Document', value=new_col)
            # print(df)
        return tf_doc       
    
    def inverse_document_frequency(self, term, all_documents):
        num_documents_with_this_term = sum(1 for doc in all_documents if term in doc["preprocessed"])
        if num_documents_with_this_term > 0:
            return 1.0 + math.log(float(len(all_documents)) / num_documents_with_this_term)
        else:
            return 1.0

    def compute_idf(self, documents):
        idf_dict = {}
        all_words = set().union(*(doc["preprocessed"] for doc in documents))
        for word in all_words:
            idf_dict[word] = self.inverse_document_frequency(word, documents)
        return idf_dict

    def compute_tfidf_with_alldocs(self, query):
        tf_idf = []
        index = 0
        self.df = pd.DataFrame(columns=['doc'] + query)
        for doc in self.documents:
            self.df['doc'] = np.arange(0, len(self.documents))
            doc_num = self.tf_doc[index]
            preprocessed_doc = doc["preprocessed"]
            for word in preprocessed_doc:
                for text in query:
                    if text == word:
                        idx = preprocessed_doc.index(word)
                        tf_idf_score = doc_num[word] * self.idf_dict[word]
                        tf_idf.append(tf_idf_score)
                        self.df.iloc[index, self.df.columns.get_loc(word)] = tf_idf_score
            index += 1
        self.df.fillna(0, axis=1, inplace=True)
        # print(self.df)
        return tf_idf, self.df

    def compute_query_tf(self, query):
        for word in query:
            self.query_norm_tf[word] = self.term_frequency(word, query)
        return self.query_norm_tf

    def compute_query_idf(self, query):        
        for word in query:         
            self.idf_dict_qry[word] = self.inverse_document_frequency(word, self.documents)
        return self.idf_dict_qry

    def compute_query_tfidf(self, query):
        for word in query:
            self.tfidf_dict_qry[word] = self.query_norm_tf[word] * self.idf_dict_qry[word]
        return self.tfidf_dict_qry    