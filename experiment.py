import math

# Membuat dokumen yang akan dijadikan korpus
dokumen1 = "Saya suka makan nasi goreng"
dokumen2 = "Saya lebih suka makan mie goreng"
dokumen3 = "Nasi goreng adalah makanan favorit saya"
dokumen4 = "Mie goreng adalah makanan kesukaan saya"

# Membuat korpus dengan dokumen-dokumen yang sudah dibuat
korpus = [dokumen1, dokumen2, dokumen3, dokumen4]

# Fungsi untuk menghitung pembobotan TF-IDF
def hitung_tf_idf(term, dokumen, korpus):
    tf = dokumen.count(term) / len(dokumen.split())
    idf = math.log(len(korpus) / (sum([1 for d in korpus if term in d])))
    print(f"{term}\t\tTF: {tf:.2f}\tIDF: {idf:.2f}")
    return tf * idf

# Fungsi untuk menghitung nilai bobot dari tiap kata pada suatu dokumen
def hitung_bobot_query(query, dokumen, korpus):
    bobot = 0
    print(f"{'Kata':<15}{'TF-IDF':<15}")
    for term in query.split():
        if term in dokumen:
            tf_idf = hitung_tf_idf(term, dokumen, korpus)
            bobot += tf_idf
            print(f"{term:<15}{tf_idf:<15.2f}")
        else:
            print(f"{term:<15}Tidak ditemukan pada dokumen")
    print(f"Total bobot query: {bobot:.2f}")
    return bobot

# Fungsi untuk mencari dokumen yang paling relevan dengan query
def cari_dokumen(query, korpus):
    skor_dokumen = []
    print(f"\nMencari dokumen dengan query '{query}':")
    for i, dokumen in enumerate(korpus):
        skor = hitung_bobot_query(query, dokumen, korpus)
        skor_dokumen.append(skor)
        print(f"Skor dokumen {i+1}: {skor:.2f}\n")
    dokumen_relevan = skor_dokumen.index(max(skor_dokumen))
    return dokumen_relevan

# Contoh penggunaan dengan beberapa query yang berbeda
query1 = "suka makan nasi"
query2 = "makanan favorit"
query3 = "mie goreng"
def hitung_bobot_query(query, dokumen, korpus):
    bobot = 0
    print(f"{'Kata':<15}{'TF-IDF':<15}")
    for term in query.split():
        if term in dokumen:
            tf_idf = hitung_tf_idf(term, dokumen, korpus)
            bobot += tf_idf * query.count(term) / len(query.split())
            print(f"{term:<15}{tf_idf * query.count(term) / len(query.split()):<15.2f}")
        else:
            print(f"{term:<15}Tidak ditemukan pada dokumen")
    print(f"Total bobot query: {bobot:.2f}")
    return bobot

# Fungsi untuk mencari dokumen yang paling relevan dengan query
def cari_dokumen(query, korpus):
    skor_dokumen = []
    print(f"\nMencari dokumen dengan query '{query}':")
    for i, dokumen in enumerate(korpus):
        skor = hitung_bobot_query(query, dokumen, korpus)
        skor_dokumen.append(skor)
        print(f"Skor dokumen {i+1}: {skor:.2f}\n")
    dokumen_relevan = skor_dokumen.index(max(skor_dokumen))
    return dokumen_relevan

# Contoh penggunaan dengan beberapa query yang berbeda
query1 = "suka makan nasi"
query2 = "makanan favorit"
query3 = "mie goreng"

dokumen_relevan = cari_dokumen(query1, korpus)
print(f"Dokumen yang paling relevan dengan query '{query1}': Dokumen {dokumen_relevan+1}\n")

dokumen_relevan = cari_dokumen(query2, korpus)
print(f"Dokumen yang paling relevan dengan query '{query2}': Dokumen {dokumen_relevan+1}\n")

dokumen_relevan = cari_dokumen(query3, korpus)
print(f"Dokumen yang paling relevan dengan query '{query3}': Dokumen {dokumen_relevan+1}\n")
