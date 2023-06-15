class JaccardSimilarity:
    def calculate(self, query, document):
        query_set = set(query)
        document_set = set(document)
        intersection = query_set.intersection(document_set)
        union = query_set.union(document_set)
        similarity = len(intersection) / len(union)
        return similarity    