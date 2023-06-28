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
        surah_instance = Surah(name=surah["name"], translation=surah["translation"], revelation=surah["revelation"], numberOfAyahs=surah["numberOfAyahs"])
        db.add(surah_instance)

        for ayah in surah["ayahs"]:
            ayah_instance = Ayah(
                surah_id=surah["number"],
                numberInQuran=ayah["number"]["inQuran"],
                numberInSurah=ayah["number"]["inSurah"],
                arabic=ayah["arabic"],
                preprocessed=",".join(ayah["preprocced"]),
                tafsir_preprocessed=",".join(ayah["tafsir_preprocessed"]),
                translation=ayah["translation"],
                tafsir=ayah["tafsir"],
            )
            db.add(ayah_instance)

    db.commit()
    
def get_all_surahs():
    all_surahs = db.query(Surah).all()
    return [surah.to_dict() for surah in all_surahs]


def get_all_ayahs_by_surah_id(surah_id:int):
    surah_data = db.query(Surah).filter(Surah.id == surah_id).first()
    all_ayahs = db.query(Ayah).filter(Ayah.surah_id == surah_id).all()
    return {
        "id": surah_data.id,
        "name": surah_data.name,
        "translation": surah_data.translation,
        "revelation": surah_data.revelation,
        "numberOfAyahs": surah_data.numberOfAyahs,        
        "ayahs": [
            {
                "id": ayah.id,
                "surah_id": ayah.surah_id,
                "number_in_quran": ayah.numberInQuran,
                "number_in_surah": ayah.numberInSurah,
                "arabic": ayah.arabic,
                "translation": ayah.translation,
                "tafsir": ayah.tafsir
            }
            for ayah in all_ayahs
        ]
    }

def get_all_ayahs():
    all_ayahs = db.query(Ayah).all()
    return [ayah.to_dict() for ayah in all_ayahs]

def get_surah_name_by_id(surah_id):
    surah = db.query(Surah).filter(Surah.id == surah_id).first()
    return surah.name
