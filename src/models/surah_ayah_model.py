class Surah:
    def __init__(self, id, name, translation, revelation, numberOfAyahs):
        self.id = id
        self.name = name
        self.translation = translation
        self.revelation = revelation
        self.numberOfAyahs = numberOfAyahs
        self.ayahs = []

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "translation": self.translation,
            "revelation": self.revelation,
            "numberOfAyahs": self.numberOfAyahs,
        }


class Ayah:
    def __init__(self, id, surah_id, numberInQuran, numberInSurah, arabic, preprocessed, tafsir_preprocessed, translation, tafsir):
        self.id = id
        self.surah_id = surah_id
        self.numberInQuran = numberInQuran
        self.numberInSurah = numberInSurah
        self.arabic = arabic
        self.preprocessed = preprocessed
        self.tafsir_preprocessed = tafsir_preprocessed
        self.translation = translation
        self.tafsir = tafsir

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
            "tafsir_preprocessed": self.tafsir_preprocessed.split(","),
            "translation": self.translation,
            "tafsir": self.tafsir,
        }

    def set_surah(self, surah):
        self.surah = surah


