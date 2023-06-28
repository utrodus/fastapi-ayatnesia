import sys, os
sys.path.append("src")
from database.database import db
from models.surah_ayah_model import Ayah
import time
from gensim.models import FastText

root_folder = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
trained_model_folder_path = os.path.join(root_folder, "src", "similarity_measure", "semantic", "trained_model")

def train_and_save_fasttext_model():
    # Ambil data ayat dan tafsir
    ayahs = db.query(Ayah).all()
    data = [(ayah.preprocessed.split() + ayah.tafsir_preprocessed.split()) for ayah in ayahs]

    # Catat waktu mulai pembuatan model
    start_time = time.time()

    # Pelatihan model FastText
    model = FastText(data, min_count=1, vector_size=100, workers=4, sg=1)

    # Hitung waktu yang dibutuhkan untuk pembuatan model
    elapsed_time = time.time() - start_time

    # Simpan model ke file biner (.bin)
    model.save(os.path.join(trained_model_folder_path, "fasttext_quran_model.bin"))


    # Tampilkan waktu yang dibutuhkan
    print("Waktu pembuatan model: %s detik" % elapsed_time)

# run the code for training and saving the model
train_and_save_fasttext_model()