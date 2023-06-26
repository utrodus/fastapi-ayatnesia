# import os
# import sqlite3

# from models.surah_ayah_model import Surah, Ayah

# current_path = os.path.join(os.path.dirname(os.path.realpath(__file__)))
# db_file_path = os.path.abspath(os.path.join(current_path, "quran.db"))

# connection = sqlite3.connect(db_file_path)
# cursor = connection.cursor()


# def check_database_connection():
#     try:
#         connection.execute("SELECT 1")
#         return True
#     except sqlite3.OperationalError:
#         return False


# def write_quran_db(surahs):
#     for surah in surahs:
#         surah_instance = Surah(
#             name=surah["name"],
#             translation=surah["translation"],
#             revelation=surah["revelation"],
#             numberOfAyahs=surah["numberOfAyahs"],
#         )
#         cursor.execute(
#             "INSERT INTO surah (name, translation, revelation, numberOfAyahs) VALUES (?, ?, ?, ?)",
#             (surah_instance.name, surah_instance.translation, surah_instance.revelation, surah_instance.numberOfAyahs),
#         )
#         surah_id = cursor.lastrowid

#         for ayah in surah["ayahs"]:
#             ayah_instance = Ayah(
#                 surah_id=surah_id,
#                 numberInQuran=ayah["number"]["inQuran"],
#                 numberInSurah=ayah["number"]["inSurah"],
#                 arabic=ayah["arabic"],
#                 preprocessed=",".join(ayah["preprocessed"]),
#                 tafsir_preprocessed=",".join(ayah["tafsir_preprocessed"]),
#                 translation=ayah["translation"],
#                 tafsir=ayah["tafsir"],
#             )
#             cursor.execute(
#                 "INSERT INTO ayahs (surah_id, numberInQuran, numberInSurah, arabic, preprocessed, tafsir_preprocessed, translation, tafsir) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
#                 (
#                     ayah_instance.surah_id,
#                     ayah_instance.numberInQuran,
#                     ayah_instance.numberInSurah,
#                     ayah_instance.arabic,
#                     ayah_instance.preprocessed,
#                     ayah_instance.tafsir_preprocessed,
#                     ayah_instance.translation,
#                     ayah_instance.tafsir,
#                 ),
#             )

#     connection.commit()


# def get_all_surahs():
#     cursor.execute("SELECT * FROM surah")
#     all_surahs = cursor.fetchall()
#     return [
#         {
#             "id": surah[0],
#             "name": surah[1],
#             "translation": surah[2],
#             "revelation": surah[3],
#             "numberOfAyahs": surah[4],
#         }
#         for surah in all_surahs
#     ]


# def get_all_ayahs_by_surah_id(surah_id: int):
#     cursor.execute("SELECT * FROM surah WHERE id = ?", (surah_id,))
#     surah_data = cursor.fetchone()

#     cursor.execute("SELECT * FROM ayahs WHERE surah_id = ?", (surah_id,))
#     all_ayahs = cursor.fetchall()

#     return {
#         "id": surah_data[0],
#         "name":surah_data[1],
#         "translation": surah_data[2],
#         "revelation": surah_data[3],
#         "numberOfAyahs": surah_data[4],
#         "ayahs": [
#             {
#                 "id": ayah[0],
#                 "surah_id": ayah[1],
#                 "number_in_quran": ayah[2],
#                 "number_in_surah": ayah[3],
#                 "arabic": ayah[4],
#                 "translation": ayah[7],
#                 "tafsir": ayah[8],
#             }
#             for ayah in all_ayahs
#         ],
#     }


# def get_all_ayahs():
#     cursor.execute("SELECT * FROM ayahs")
#     all_ayahs = cursor.fetchall()
#     return [
#         {
#             "id": ayah[0],
#             "surah_id": ayah[1],
#             "number_in_quran": ayah[2],
#             "number_in_surah": ayah[3],
#             "arabic": ayah[4],
#             "translation": ayah[7],
#             "tafsir": ayah[8],
#         }
#         for ayah in all_ayahs
#     ]


# def get_surah_name_by_id(surah_id):
#     cursor.execute("SELECT name FROM surah WHERE id = ?", (surah_id,))
#     surah = cursor.fetchone()
#     return surah[0]
import os
import sqlite3

from models.surah_ayah_model import Surah, Ayah

current_path = os.path.join(os.path.dirname(os.path.realpath(__file__)))
db_file_path = os.path.abspath(os.path.join(current_path, "quran.db"))

connection = sqlite3.connect(db_file_path)
cursor = connection.cursor()


def check_database_connection():
    try:
        connection.execute("SELECT 1")
        return True
    except sqlite3.OperationalError:
        return False


def write_quran_db(surahs):
    for surah in surahs:
        surah_instance = Surah(
            id=surah["id"],
            name=surah["name"],
            translation=surah["translation"],
            revelation=surah["revelation"],
            numberOfAyahs=surah["numberOfAyahs"],
        )
        cursor.execute(
            "INSERT INTO surah (id, name, translation, revelation, numberOfAyahs) VALUES (?, ?, ?, ?, ?)",
            (
                surah_instance.id,
                surah_instance.name,
                surah_instance.translation,
                surah_instance.revelation,
                surah_instance.numberOfAyahs,
            ),
        )

        for ayah in surah["ayahs"]:
            ayah_instance = Ayah(
                id=ayah["id"],
                surah_id=surah_instance.id,
                numberInQuran=ayah["number"]["inQuran"],
                numberInSurah=ayah["number"]["inSurah"],
                arabic=ayah["arabic"],
                preprocessed=",".join(ayah["preprocessed"]),
                tafsir_preprocessed=",".join(ayah["tafsir_preprocessed"]),
                translation=ayah["translation"],
                tafsir=ayah["tafsir"],
            )
            cursor.execute(
                "INSERT INTO ayahs (id, surah_id, numberInQuran, numberInSurah, arabic, preprocessed, tafsir_preprocessed, translation, tafsir) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                (
                    ayah_instance.id,
                    ayah_instance.surah_id,
                    ayah_instance.numberInQuran,
                    ayah_instance.numberInSurah,
                    ayah_instance.arabic,
                    ayah_instance.preprocessed,
                    ayah_instance.tafsir_preprocessed,
                    ayah_instance.translation,
                    ayah_instance.tafsir,
                ),
            )

    connection.commit()


def get_all_surahs():
    cursor.execute("SELECT * FROM surah")
    all_surahs = cursor.fetchall()
    return [
        Surah(
            id=surah[0],
            name=surah[1],
            translation=surah[2],
            revelation=surah[3],
            numberOfAyahs=surah[4],
        ).to_dict()
        for surah in all_surahs
    ]


def get_all_ayahs_by_surah_id(surah_id: int):
    cursor.execute("SELECT * FROM surah WHERE id = ?", (surah_id,))
    surah_data = cursor.fetchone()

    cursor.execute("SELECT * FROM ayahs WHERE surah_id = ?", (surah_id,))
    all_ayahs = cursor.fetchall()

    return {
        "id": surah_data[0],
        "name":surah_data[1],
        "translation": surah_data[2],
        "revelation": surah_data[3],
        "numberOfAyahs": surah_data[4],
        "ayahs": [
            {
                "id": ayah[0],
                "surah_id": ayah[1],
                "number_in_quran": ayah[2],
                "number_in_surah": ayah[3],
                "arabic": ayah[4],
                "translation": ayah[7],
                "tafsir": ayah[8],
            }
            for ayah in all_ayahs
        ],
    }


def get_all_ayahs():
    cursor.execute("SELECT * FROM ayahs")
    all_ayahs = cursor.fetchall()
    return [
        Ayah(
            id=ayah[0],
            surah_id=ayah[1],
            numberInQuran=ayah[2],
            numberInSurah=ayah[3],
            arabic=ayah[4],
            preprocessed=ayah[5],
            tafsir_preprocessed=ayah[6],
            translation=ayah[7],
            tafsir=ayah[8],
        ).to_dict()
        for ayah in all_ayahs
    ]


def get_surah_name_by_id(surah_id):
    cursor.execute("SELECT name FROM surah WHERE id = ?", (surah_id,))
    surah = cursor.fetchone()
    return surah[0]
