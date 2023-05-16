import sqlite3
import os
import psutil


current_path = os.path.join(os.path.dirname(os.path.realpath(__file__)))
quran_preprocessed_db_path = os.path.abspath(
    os.path.join(current_path, "data/quran.db")
)

# Connect to SQLite database
conn = sqlite3.connect(quran_preprocessed_db_path)
c = conn.cursor()

# test connection
def test_connections():
    for proc in psutil.process_iter():
        try:
            files = proc.get_open_files()
            if files:
                for _file in files:
                    if _file.path == quran_preprocessed_db_path:
                        return True
        except psutil.NoSuchProcess as err:
            print(err)
    return False

# write quran db
def write_quran_db(surahs):
    # Create the surah table
    c.execute(
        """CREATE TABLE surah (
                id INTEGER PRIMARY KEY,
                number INTEGER,
                name TEXT,
                translation TEXT
                )"""
    )

    # Create the ayahs table
    c.execute(
        """CREATE TABLE ayahs (
                id INTEGER PRIMARY KEY,
                surah_id INTEGER,
                numberInQuran INTEGER,
                numberInSurah INTEGER,
                arabic TEXT,
                preprocessed TEXT,
                translation TEXT,
                tafsir TEXT,
                FOREIGN KEY(surah_id) REFERENCES surah(id)
                )"""
    )

    # Insert surahs into the surah table and ayahs into the ayahs table
    for surah in surahs:
        surah_values = (
            surah["number"],
            surah["name"],
            surah["translation"],
        )
        c.execute(
            "INSERT INTO surah (number, name, translation) VALUES (?, ?, ?)",
            surah_values,
        )

        surah_id = c.lastrowid
        for ayah in surah["ayahs"]:
            ayah_values = (
                surah_id,
                ayah["number"]["inQuran"],
                ayah["number"]["inSurah"],
                ayah["arabic"],
                ",".join(ayah["preprocced"]),
                ayah["translation"],
                ayah["tafsir"],
            )
            c.execute(
                "INSERT INTO ayahs (surah_id, numberInQuran, numberInSurah, arabic, preprocessed, translation, tafsir) VALUES (?, ?, ?, ?, ?, ?, ?)",
                ayah_values,
            )

    # Commit the changes
    conn.commit()

    # Close the connection
    conn.close()
    
def read_all_surahs():
    c.execute("SELECT * FROM surah")
    all_surahs = c.fetchall()
    
    result = []
    for item in all_surahs:
        dictionary = {
            "id": item[0],
            "number": item[1],
            "name": item[2],
            "translation": item[3]
        }
        result.append(dictionary)
    return result    

