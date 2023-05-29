import numpy as np
import math
import pandas as pd

class TfIdf:
    def __init__(self, quran_documents: list, query: str):
        """
        Menginisialisasi kelas TfIdf.
        
        Args:
            dokumen_quran (list): Sebuah daftar dokumen Quran.
            query (str): String query untuk perhitungan TF-IDF.
        """
        self.query = query
        self.quran_documents = quran_documents
    
    def termFrequency(self, term: str , document: list):
        """
        Menghitung frekuensi term (TF) dari sebuah term dalam sebuah dokumen.

        Args:
            term (str): Term yang akan dihitung frekuensinya.
            dokumen (list): Daftar term dalam dokumen.

        Returns:
            float: Frekuensi term dari term dalam dokumen.
        """      
        return document.count(term) / float(len(document))
    
    def document_frequency(self, term: str):
        """
        Menghitung frekuensi dokumen (DF) dari sebuah term dalam dokumen-dokumen Quran.

        Args:
            term (str): Term yang akan dihitung frekuensi dokumennya.

        Returns:
            int: Frekuensi dokumen dari term dalam dokumen-dokumen Quran.
        """
        df = 0
        for doc in self.quran_documents:
            if term in doc['preprocessed']:
                df += 1
        return df
    
    def compute_normalizedtf(self):
        """
        Menghitung frekuensi term yang sudah dinormalisasi (TF) untuk setiap dokumen dalam dokumen-dokumen Quran.
        """
        tf_doc = []
        doc_number = 0
        for doc in self.quran_documents:
            doc_number += 1
            ayah_preprocessed = doc['preprocessed']
            norm_tf= dict.fromkeys(set(ayah_preprocessed), 0)
            for term in ayah_preprocessed:
                norm_tf[term] = self.termFrequency(term, ayah_preprocessed)
            tf_doc.append(norm_tf)
            df = pd.DataFrame([norm_tf])
            idx = 0             
            df.insert(loc=idx, column='Document', value=doc_number)
        self.tf_doc = tf_doc
        
    def inverseDocumentFrequency(self,term:str):
        """
        Menghitung inverse document frequency (IDF) dari sebuah term dalam dokumen-dokumen Quran.

        Args:
            term (str): Term yang akan dihitung inverse document frequency-nya.

        Returns:
            float: Inverse document frequency dari term dalam dokumen-dokumen Quran.
        """
        numDocumentsWithThisTerm = self.document_frequency(term)           
        if numDocumentsWithThisTerm > 0:
            return 1.0 + math.log(float(len(self.quran_documents)) / numDocumentsWithThisTerm)
        else:
            return 1.0                
    
    def compute_idf(self):
         """
         Menghitung inverse document frequency (IDF) untuk semua term dalam dokumen-dokumen Quran.
         """
         idf_dict = {}
         for doc in self.quran_documents:
             ayah_preprocessed = doc['preprocessed']
             for term in ayah_preprocessed:
                 idf_dict[term] = self.inverseDocumentFrequency(term)
         self.idf_dict = idf_dict                 
    
    def compute_tfidf_with_alldocs(self):
        """
        Menghitung skor TF-IDF untuk semua dokumen terhadap string query.
        
        Returns:
            list: Sebuah daftar skor TF-IDF untuk setiap dokumen.
            pandas.DataFrame: Sebuah DataFrame yang berisi skor TF-IDF untuk setiap dokumen dan term query.
        """
        tf_idf = []
        index = 0
        query_tokens = self.query
        df = pd.DataFrame(columns=['doc'] + query_tokens)
        for doc in self.quran_documents:
            df['doc'] = np.arange(0 , len(self.quran_documents))
            doc_num = self.tf_doc[index]
            ayah_preprocessed = doc['preprocessed']
            for term_ayah in ayah_preprocessed:
                for term_query in query_tokens:
                    if(term_query == term_ayah):
                        idx = ayah_preprocessed.index(term_ayah)
                        tf_idf_score = doc_num[term_ayah] * self.idf_dict[term_ayah]
                        tf_idf.append(tf_idf_score)
                        df.iloc[index, df.columns.get_loc(term_ayah)] = tf_idf_score
            index += 1
        df.fillna(0 , axis=1, inplace=True)
        print(df)
        return tf_idf , df
    
    def compute_query_tf_normalize(self):
        query_norm_tf = {}        
        for word in self.query:
            query_norm_tf[word] = self.termFrequency(word , self.query)
        self.query_norm_tf = query_norm_tf            
        return query_norm_tf
    
    def compute_query_idf(self):
        idf_dict_qry = {}                
        for word in self.query:
            idf_dict_qry[word] = self.inverseDocumentFrequency(word)
        self.idf_dict_qry = idf_dict_qry            
        return idf_dict_qry
    
    def compute_query_tfidf(self):
        tfidf_dict_qry = {}        
        for word in self.query:
            tfidf_dict_qry[word] = self.query_norm_tf[word] * self.idf_dict_qry[word]
        print(tfidf_dict_qry)            
        return tfidf_dict_qry       
    
    def execute_tfidf_all_docs(self):
        self.compute_normalizedtf()
        self.compute_idf()
        self.compute_tfidf_with_alldocs()
    
    def execute_tfidf_query(self):
        self.compute_query_tf_normalize()
        self.compute_query_idf()
        self.compute_query_tfidf()        

quran_documents = [ {'preprocessed': ["dengan","nama","allah","maha","asih","maha","sayang"]},
                   {'preprocessed': ["puji","allah","tuhan","alam" ]},
                   {'preprocessed': ["maha","asih","maha","sayang"]} ] 
       
tf_idf = TfIdf(quran_documents, ['maha', 'asih'])
print(tf_idf.execute_tfidf_query())