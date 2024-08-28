from fastapi import FastAPI,Request, Query, status
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.openapi.utils import get_openapi

import re
import sys

sys.path.append("src")
from src.database.database import check_database_connection, get_all_surahs, get_all_ayahs_by_surah_id, get_all_ayahs
from src.preprocessing.preprocessing import Preprocessing
from src.models.search_result_model import SearchResult
from src.similarity_measure.lexical.lexical_measure import LexicalMeasure
from src.similarity_measure.semantic.semantic_measure import SemanticMeasure, WordEmbedding
from src.similarity_measure.lexical_semantic.lexical_semantic_measure import LexicalSemanticMeasure
import time

templates = Jinja2Templates(directory="views")

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

origins = ['*']
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.title = (
    "AyatNesia API for searching Quranic verses"
)
app.description = (
    """
The AyatNesia API allows you to search for text using various measures such as lexical, semantic, and lexical semantic.

It provides an efficient way to access and retrieve information from the Quran.

*The API empowers you with these features to enhance your search capabilities and facilitate a comprehensive analysis of the Quran. 🚀*

## 💎 Key Features:

- **Get All Qur'an Surahs**: Retrieve the list of all Surahs (chapters) in the Quran.

- **Get Surah Details**: Get detailed information about a specific Surah, including its verses (Ayahs) and other metadata.

- **Search Using Lexical Measures**: Perform a search based on lexical similarity, finding verses that are lexically similar to the query text.

- **Search Using Semantic Measures**: Conduct a search based on semantic similarity, identifying verses that are semantically related to the query text.

- **Search Using Lexical-Semantic Measures**: Utilize a combined approach of lexical and semantic measures for more accurate and comprehensive search results.

## 📞 Contact Us
If you have any questions, feedback, or need assistance regarding the AyatNesia API, please don't hesitate to [contact us](https://www.utrodus.com/). We are here to help you!

    """
)
app.version = "1"
app.debug = False


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
@app.get("/", tags=["🌐 Web App for AyatNesia"], include_in_schema=False)
async def home(request: Request):
    """
    ## 🏠 Endpoint that redirects to the home page.
    """
    return templates.TemplateResponse("index.html", {"request": request, "all_surahs": all_surah})

@app.get("/detail-surah/{id}", tags=["🌐 Web App for AyatNesia"], include_in_schema=False)
async def detail_surah(request: Request, id: int):
    """
    ## 📜 Endpoint that redirects to the detail surah page.
    """
    detail_surah = get_all_ayahs_by_surah_id(id)
    return templates.TemplateResponse("detail_surah.html", {"request": request, "all_surahs": all_surah, "detail_surah": detail_surah})

@app.get("/search", tags=["🌐 Web App for AyatNesia"], include_in_schema=False)
async def search(request: Request):
    """
    ## 🔍 Endpoint that redirects to the search page.
    """
    return templates.TemplateResponse("search.html", {"request": request, "all_surahs": all_surah})



# API Endpoints

@app.get("/api/docs", include_in_schema=False)
async def get_documentation():
    return get_swagger_ui_html(openapi_url="/openapi.json", title="Swagger")

@app.get("/openapi.json", include_in_schema=False)
async def openapi():
    return get_openapi(title=app.title, version=app.version, routes=app.routes)

@app.get("/api/test-connection", tags=["🔌 API: Test Connection"],status_code=status.HTTP_200_OK)
async def test_connections():
    """
    ## Test the connection to the AyatNesia API. ⚡️

    ### Returns:
        - 200 OK: If the connection is successful.
        - 500 Internal Server Error: If the API fails to connect to the database.
    """
    connections_status = check_database_connection()
    if connections_status:
        return {"message": "AyatNesia API is running. ✅"}
    else:
        return JSONResponse(status_code=500, content={"detail": "AyatNesia API is not running. Failed to connect to the database"})


@app.get("/api/all-surahs", tags=["📃 API: Get Surahs and Detail"])
async def get_list_surah():
    """
    ## Get the list of all surahs. 📚

    ### Returns:
        - 200 OK: List of all surahs.
        - 500 Internal Server Error: If there's an error retrieving the surahs.
    """
    try:
        return all_surah
    except Exception as e:
        return JSONResponse(status_code=500, content={"detail": f"Failed to retrieve surahs. Error: {str(e)}"})


@app.get("/api/detail/{surah_id}", tags=["📃 API: Get Surahs and Detail"])
async def get_surah(surah_id: int):
    """
    ## Get the detail of a surah by its ID. 📖

    ### Parameters:
        - surah_id (int): The ID of the surah.

    ### Returns:
        - 200 OK: Detail of the surah.
        - 500 Internal Server Error: If there's an error retrieving the surah details.
    """
    try:
        ayahs = get_all_ayahs_by_surah_id(surah_id)
        return ayahs
    except Exception as e:
        return JSONResponse(status_code=500, content={"detail": f"Failed to retrieve surah details. Error: {str(e)}"})


@app.post("/api/search", tags=["🔎 API: Search Feature"])
async def search(query: str, measure_type: str = Query("combination", title="Measure Type", description="Measure type to be used: lexical, semantic, combination"), top_relevance=Query("all", title="Top Relevance", description="Filter Top Relevance: the number of results returned (all, 5, 10, 15)")):
    """
    ## Perform a search based on the query and measure type. 🔍

    ### Parameters:
        - query (str): The search query.
        - measure_type (str): Measure type to be used: lexical, semantic, combination.
        - top_relevance (str): Filter Top Relevance: the number of results returned (all, 5, 10, 15).

    ### Returns:
        - 200 OK: Search results.
        - 400 Bad Request: If the query is empty or the measure type is invalid.
        - 500 Internal Server Error: If there's an error during the search process.
    """
    measure_type = re.sub(r"\s+", "", measure_type.lower(), flags=re.UNICODE)
    if query == "":
        return JSONResponse(status_code=400, content={"detail": "Kata kunci tidak boleh kosong."})
    else:
        query_preprocessed = Preprocessing(query).execute()

        if measure_type == "lexical":
            start_time = time.time()
            results = lexical_measure.get_top_similarities(query_preprocessed, top_relevance)
            end_time = time.time()
            execution_time = end_time - start_time
            response = SearchResult(execution_time=execution_time, results=results)
            return response
        elif measure_type == "semantic":
            start_time = time.time()
            results = semantic_measure.get_top_similarities(query_preprocessed, top_relevance)
            end_time = time.time()
            execution_time = end_time - start_time
            response = SearchResult(execution_time=execution_time, results=results)
            return response
        elif measure_type == "combination":
            start_time = time.time()
            results = lexical_semantic_measure.get_top_similarities(query_preprocessed, top_relevance)
            end_time = time.time()
            execution_time = end_time - start_time
            response = SearchResult(execution_time=execution_time, results=results)
            return response
        else:
            return JSONResponse(status_code=400, content={"detail": "Measure type tidak ditemukan."})
        
