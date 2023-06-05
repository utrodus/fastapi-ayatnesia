from fastapi import FastAPI, Query, HTTPException
from pydantic import Field

import sys
sys.path.append("src")
from src.database.database import check_database_connection, get_all_surahs, get_all_ayahs_by_surah_id
from src.preprocessing.preprocessing import Preprocessing
from src.similarity_measure.lexical.lexical_measure import LexicalMeasure

app = FastAPI()
app.title = (
    "Quran Search API for searching Quranic verses"
)
app.description = (
    """

## Quran Search API

The Quran Search API allows you to search for text using various measures such as lexical, semantic, and lexical semantic.

It provides an efficient way to access and retrieve information from the Quran.

*The API empowers you with these features to enhance your search capabilities and facilitate a comprehensive analysis of the Quran. 🚀*

## 💎 Key Features:

-   Get all Qur'an Surahs (✅ done).
-   Get detailed information about a specific Quran Surah (✅ done).
-   Search using lexical measures (✅ done).
-   Search using semantic measures (⏳ _in progress_).
-   Search using lexical semantic measures (⏳ _in progress_).

    """
)
app.version = "0.0.1"
app.debug = True

@app.get("/", tags=["1. Test Connection"])
def root():
    return {"message": "Welcome to Quran Finder API. Please go to /docs for more info."}

@app.get("/test-connection", tags=["1. Test Connection"])
async def test_connections():
    connections_status = check_database_connection()
    if(connections_status):
        return {"message": "Quran Finder API is running. "}
    else:
        raise HTTPException(status_code=500, detail="Quran Finder API is not running, Failed to connect to the database")

@app.get("/all-surahs",  tags=["2. Get Surahs And Detail"])
async def get_list_surah():
    all_surah = get_all_surahs()
    return all_surah

@app.get("/detail/{surah_id}", tags=["2. Get Surahs And Detail"])
async def get_surah(surah_id: int):
    ayahs = get_all_ayahs_by_surah_id(surah_id)
    return ayahs

@app.post("/search", tags=["3. Search Feature"])
async def search(query: str, measure_type: str = Query("lexical", title="Measure Type", description="**Measure type** will be used: ( *lexical | semantic | lexical_semantic*)"), limit: int = Query(5, title="Limit", description="**Limit** the number of results returned. Default: 5")):
    if(query == ""):
        return {"message": "Kata kunci tidak boleh kosong."}
    else:
        query_preprocessed = Preprocessing(query).execute()
        if(measure_type == "lexical"):
            lexical_measure = LexicalMeasure()
            lexical_measure.calculate_lexical_similarity(query_preprocessed)
            results = lexical_measure.get_top_similarities(limit)
            return results
        elif(measure_type == "semantic"):
            return {"query": query_preprocessed}
        else:
            return {"query": query_preprocessed}