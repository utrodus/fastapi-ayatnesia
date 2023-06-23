from fastapi import FastAPI,Request, Query, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

import re
import sys
sys.path.append("src")
from src.database.database import check_database_connection, get_all_surahs, get_all_ayahs_by_surah_id, get_all_ayahs
from src.preprocessing.preprocessing import Preprocessing
from src.similarity_measure.lexical.lexical_measure import LexicalMeasure
from src.similarity_measure.semantic.semantic_measure import SemanticMeasure, WordEmbedding
from src.similarity_measure.lexical_semantic.lexical_semantic_measure import LexicalSemanticMeasure


templates = Jinja2Templates(directory="views")

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

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


# get all ayahs from database
all_ayahs = get_all_ayahs()
# get all surahs from database
all_surah = get_all_surahs()

# initialize lexical measure
lexical_measure = LexicalMeasure(all_ayahs=all_ayahs)

# initialize semantic measure
word_embedding = WordEmbedding()
semantic_measure = SemanticMeasure(word_embedding=word_embedding, all_ayahs=all_ayahs)

# initialize lexical semantic measure
lexical_semantic_measure = LexicalSemanticMeasure(all_ayahs=all_ayahs, lexical_measure=lexical_measure, semantic_measure=semantic_measure)


# Frontend Endpoints
@app.get("/", tags=["Welcome sections"])
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "all_surahs": all_surah})

@app.get("/detail-surah/{id}")
async def detail_surah(request: Request, id:int):
    detail_surah = get_all_ayahs_by_surah_id(id)
    return templates.TemplateResponse("detail_surah.html", {"request": request, "all_surahs": all_surah, "detail_surah": detail_surah})

@app.get("/search")
async def search(request: Request):
    return templates.TemplateResponse("search.html", {"request": request, "all_surahs": all_surah})

@app.get("/search-result")
async def search_result(request: Request):
    return templates.TemplateResponse("search.html", {"request": request, "all_surahs": all_surah})
    
# API Endpoints
@app.get("/api/test-connection", tags=["1. Test Connection"])
async def test_connections():
    connections_status = check_database_connection()
    if(connections_status):
        return {"message": "AyatNesia API is running. "}
    else:
        raise HTTPException(status_code=500, detail="AyatNesia API is not running, Failed to connect to the database")

@app.get("/api/all-surahs",  tags=["2. Get Surahs And Detail"])
async def get_list_surah():
    try:        
        return all_surah
    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to retrieve surahs. Error: {}".format(str(e)))

@app.get("/api/detail/{surah_id}", tags=["2. Get Surahs And Detail"])
async def get_surah(surah_id: int):
    try:
        ayahs = get_all_ayahs_by_surah_id(surah_id)
        return ayahs
    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to retrieve surah details. Error: {}".format(str(e)))
    


@app.post("/api/search", tags=["3. Search Feature"])
async def search(query: str, 
                 measure_type: str = Query("combination", title="Measure Type", description="**Measure type** will be used: ( *lexical | semantic | combination*)"), 
                 top_relevance = Query("all", title="Top Relevance", description="**Filter Top Relevance:** the number of results returned (all | 5 | 10 | 15)"),
                 ):
                 
    measure_type =  re.sub(r"\s+", "", measure_type.lower(), flags=re.UNICODE)
    if(query == ""):
        raise HTTPException(status_code=400, detail="Kata kunci tidak boleh kosong.")
    else:
        query_preprocessed = Preprocessing(query).execute()
        
        if(measure_type == "lexical"):
            results = lexical_measure.get_top_similarities(query_preprocessed,top_relevance)
            return results
        elif(measure_type == "semantic"):
            results = semantic_measure.get_top_similarities(query_preprocessed, top_relevance)
            return {
                "results": results
            }
        elif(measure_type == "combination"):
            results = lexical_semantic_measure.get_top_similarities(query_preprocessed,top_relevance)
            return results
        else:
            raise HTTPException(status_code=400, detail="Measure type tidak ditemukan.")