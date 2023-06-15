from fastapi import FastAPI, Query, HTTPException
from fastapi.responses import HTMLResponse
import re

import sys
sys.path.append("src")
from src.database.database import check_database_connection, get_all_surahs, get_all_ayahs_by_surah_id
from src.preprocessing.preprocessing import Preprocessing
from src.similarity_measure.lexical.lexical_measure import LexicalMeasure
from src.similarity_measure.semantic.semantic_measure import SemanticMeasure


app = FastAPI()
app.title = (
    "AyatNesia API for searching Quranic verses"
)
app.description = (
    """
The AyatNesia API allows you to search for text using various measures such as lexical, semantic, and lexical semantic.

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


@app.get("/", tags=["Welcome sections"], response_class=HTMLResponse)
def root():
    html_content = """
    <html>
    <head>
        <title>Welcome to AyatNesia API</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                background-color: #f2f2f2;
                padding: 20px;
                text-align: center;
            }
            h1 {
                color: #333333;
            }
            p {
                color: #666666;
                margin-bottom: 20px;
            }
            .link {
                color: #0000EE;
                text-decoration: underline;
            }
        </style>
    </head>
    <body>
        <h1>Welcome to AyatNesia API</h1>
        <p>Please go to <a href="/docs" class="link">/docs</a> for more information.</p>
    </body>
    </html>
    """
    return html_content

@app.get("/test-connection", tags=["1. Test Connection"])
async def test_connections():
    connections_status = check_database_connection()
    if(connections_status):
        return {"message": "AyatNesia API is running. "}
    else:
        raise HTTPException(status_code=500, detail="AyatNesia API is not running, Failed to connect to the database")

@app.get("/all-surahs",  tags=["2. Get Surahs And Detail"])
async def get_list_surah():
    try:
        all_surah = get_all_surahs()
        return all_surah
    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to retrieve surahs. Error: {}".format(str(e)))

@app.get("/detail/{surah_id}", tags=["2. Get Surahs And Detail"])
async def get_surah(surah_id: int):
    try:
        ayahs = get_all_ayahs_by_surah_id(surah_id)
        return ayahs
    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to retrieve surah details. Error: {}".format(str(e)))

@app.post("/search", tags=["3. Search Feature"])
async def search(query: str, measure_type: str = Query("lexical", title="Measure Type", description="**Measure type** will be used: ( *lexical | semantic | lexical_semantic*)"), limit: int = Query(5, title="Limit", description="**Limit** the number of results returned. Default: 5")):
    measure_type =  re.sub(r"\s+", "", measure_type.lower(), flags=re.UNICODE)
    print("measure_type: ", measure_type)
    if(query == ""):
        raise HTTPException(status_code=400, detail="Kata kunci tidak boleh kosong.")
    else:
        query_preprocessed = Preprocessing(query).execute()
        if(measure_type == "lexical"):
            lexical_measure = LexicalMeasure()
            lexical_measure.calculate_lexical_similarity(query_preprocessed)
            results = lexical_measure.get_top_similarities(limit)
            return results
        elif(measure_type == "semantic"):
            semantic_measure = SemanticMeasure()
            semantic_measure.calculate_semantic_similarity(query_preprocessed)
            results = semantic_measure.get_top_similarities(limit)
            return results
        else:
            raise HTTPException(status_code=400, detail="Measure type tidak ditemukan.")