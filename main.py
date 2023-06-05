from fastapi import FastAPI, Query
from pydantic import Field

import sys
sys.path.append("src")
from src.database.database import test_connections, get_all_surahs, get_all_ayahs_by_surah_id
from src.preprocessing.preprocessing import Preprocessing
from src.similarity_measure.lexical.lexical_measure import LexicalMeasure

app = FastAPI()
app.title = (
    "Quran Search API for searching Quranic verses"
)
app.description = (
    """
    Quran Search API helps you to searching text using lexical, semantic, and lexical semantic measure. 🚀
    
### Search Feature
You will be able to:

* **Get All Qur'an Surahs** (✅ done).
* **Get Detail Quran Surah** (✅ done).
* **Search using lexical measures** (✅ done).
* **Search using semantic measures** (⏳ _on progress_).
* **Search using lexical semantic measures** (⏳ _on progress_).
    """
)
app.version = "0.0.1"
app.debug = True

@app.get("/")
def root():
    return {"message": "Welcome to Quran Finder API. Please go to /docs for more info."}

@app.get("/test-connection")
async def test_connections():
    connections_status = test_connections()
    if(connections_status):
        return {"message": "Quran Finder API is running. "}
    return {"message": "Quran Finder API is not running. "}

@app.get("/all-surahs")
async def get_list_surah():
    all_surah = get_all_surahs()
    return all_surah

@app.get("/detail/{surah_id}")
async def get_surah(surah_id: int):
    ayahs = get_all_ayahs_by_surah_id(surah_id)
    return ayahs

@app.post("/search")
async def search(query: str, type: str = Query( "lexical", title="Search Type", description="type of search will be used: (**lexical** | **semantic** | **lexical_semantic**)"), limit: int = 5):
    if(query == ""):
        return {"message": "Kata kunci tidak boleh kosong."}
    else:
        query_preprocessed = Preprocessing(query).execute()
        if(type == "lexical"):
            lexical_measure = LexicalMeasure()
            lexical_measure.calculate_lexical_similarity(query_preprocessed)
            results = lexical_measure.get_top_similarities(limit)
            return results
        elif(type == "semantic"):
            return {"query": query_preprocessed}
        else:
            return {"query": query_preprocessed}