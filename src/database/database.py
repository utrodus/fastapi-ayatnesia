import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import OperationalError
from models.surah_ayah_model import Base, Surah, Ayah

current_path = os.path.join(os.path.dirname(os.path.realpath(__file__)))
db_file_path = os.path.abspath(
    os.path.join(current_path, "quran.db")
)
SQLALCHEMY_DATABASE_URL = f"sqlite:///{db_file_path}"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)
db = SessionLocal()

def check_database_connection():
    try:
        with engine.connect():
            pass
        return True
    except OperationalError:
        return False    

def write_quran_db(surahs):
    for surah in surahs:
        surah_instance = Surah(name=surah["name"], translation=surah["translation"])
        db.add(surah_instance)

        for ayah in surah["ayahs"]:
            ayah_instance = Ayah(
                surah_id=surah["number"],
                numberInQuran=ayah["number"]["inQuran"],
                numberInSurah=ayah["number"]["inSurah"],
                arabic=ayah["arabic"],
                preprocessed=",".join(ayah["preprocced"]),
                translation=ayah["translation"],
                tafsir=ayah["tafsir"],
            )
            db.add(ayah_instance)

    db.commit()

def save_word_embedding_result(ayah_id, result):
    ayah = db.query(Ayah).filter(Ayah.id == ayah_id).first()
    print(f"Saving word embedding result for ayah {ayah_id}")
    ayah.word_embedding_result = ",".join(result)
    db.commit()    

def get_all_surahs():
    all_surahs = db.query(Surah).all()
    return [surah.to_dict() for surah in all_surahs]


def get_all_ayahs_by_surah_id(surah_id):
    all_ayahs = db.query(Ayah).filter(Ayah.surah_id == surah_id).all()
    return [ayah.to_dict() for ayah in all_ayahs]


def get_all_ayahs():
    all_ayahs = db.query(Ayah).all()
    return [ayah.to_dict() for ayah in all_ayahs]

def get_surah_name_by_id(surah_id):
    surah = db.query(Surah).filter(Surah.id == surah_id).first()
    return surah.name