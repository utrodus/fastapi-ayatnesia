import math
import pandas as pd
import numpy as np

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
        normalize_document = document.lower().split()
        return normalize_document.count(term.lower()) / float(len(normalize_document))

    def compute_normalized_tf(self, documents):
        tf_doc = []
        for txt in documents:
            sentence = txt.split()
            norm_tf = dict.fromkeys(set(sentence), 0)
            for word in sentence:
                norm_tf[word] = self.term_frequency(word, txt)
            tf_doc.append(norm_tf)
            df = pd.DataFrame([norm_tf])
            idx = 0
            new_col = ["Normalized TF"]
            df.insert(loc=idx, column='Document', value=new_col)
            print(df)
        return tf_doc

    def inverse_document_frequency(self, term, all_documents):
        num_documents_with_this_term = 0
        for doc in range(0, len(all_documents)):
            if term.lower() in all_documents[doc].lower().split():
                num_documents_with_this_term = num_documents_with_this_term + 1

        if num_documents_with_this_term > 0:
            return 1.0 + math.log(float(len(all_documents)) / num_documents_with_this_term)
        else:
            return 1.0

    def compute_idf(self, documents):
        idf_dict = {}
        for doc in documents:
            sentence = doc.split()
            for word in sentence:
                idf_dict[word] = self.inverse_document_frequency(word, documents)
        return idf_dict

    def compute_tfidf_with_alldocs(self, query):
        tf_idf = []
        index = 0
        query_tokens = query.split()
        self.df = pd.DataFrame(columns=['doc'] + query_tokens)
        for doc in self.documents:
            self.df['doc'] = np.arange(0, len(self.documents))
            doc_num = self.tf_doc[index]
            sentence = doc.split()
            for word in sentence:
                for text in query_tokens:
                    if text == word:
                        idx = sentence.index(word)
                        tf_idf_score = doc_num[word] * self.idf_dict[word]
                        tf_idf.append(tf_idf_score)
                        self.df.iloc[index, self.df.columns.get_loc(word)] = tf_idf_score
            index += 1
        self.df.fillna(0, axis=1, inplace=True)
        return tf_idf, self.df

    def compute_query_tf(self, query):
        tokens = query.split()
        for word in tokens:
            self.query_norm_tf[word] = self.term_frequency(word, query)
        return self.query_norm_tf

    def compute_query_idf(self, query):
        sentence = query.split()
        for word in sentence:
            self.idf_dict_qry[word] = self.inverse_document_frequency(word, self.documents)
        return self.idf_dict_qry

    def compute_query_tfidf(self, query):
        sentence = query.split()
        for word in sentence:
            self.tfidf_dict_qry[word] = self.query_norm_tf[word] * self.idf_dict_qry[word]
        return self.tfidf_dict_qry


class CosineSimilarity:
    @staticmethod
    def compute(tfidf_dict_qry, df, query, doc_num):
        dot_product = 0
        qry_mod = 0
        doc_mod = 0
        tokens = query.split()

        for keyword in tokens:
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


documents = ["I want to start learning to charge something in life",
             "reading something about life no one else knows",
             "Never stop learning"]
query = "life learning"

tfidf = TFIDF(documents)
tf_doc = tfidf.compute_normalized_tf(documents)
idf_dict = tfidf.compute_idf(documents)
tf_idf, df = tfidf.compute_tfidf_with_alldocs(query)
print(df)
query_norm_tf = tfidf.compute_query_tf(query)
print(query_norm_tf)
idf_dict_qry = tfidf.compute_query_idf(query)
print(idf_dict_qry)
tfidf_dict_qry = tfidf.compute_query_tfidf(query)
print(tfidf_dict_qry)

similarity_docs = RankSimilarityDocs(documents, tfidf_dict_qry, df, query).compute()
doc_names = ["Document1", "Document2", "Document3"]
print(doc_names)
print(list(similarity_docs))
