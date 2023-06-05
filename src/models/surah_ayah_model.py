from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()

class Surah(Base):
    __tablename__ = "surah"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    translation = Column(String)

    ayahs = relationship("Ayah", back_populates="surah")

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "translation": self.translation,
        }


class Ayah(Base):
    __tablename__ = "ayahs"

    id = Column(Integer, primary_key=True)
    surah_id = Column(Integer, ForeignKey("surah.id"))
    numberInQuran = Column(Integer)
    numberInSurah = Column(Integer)
    arabic = Column(String)
    preprocessed = Column(String)
    translation = Column(String)
    tafsir = Column(String)

    surah = relationship("Surah", back_populates="ayahs")

    def to_dict(self):
        return {
            "id": self.id,
            "surah_id": self.surah_id,
            "number": {
                "inQuran": self.numberInQuran,
                "inSurah": self.numberInSurah,
            },
            "arabic": self.arabic,
            "preprocessed": self.preprocessed.split(","),
            "translation": self.translation,
            "tafsir": self.tafsir,
        }
