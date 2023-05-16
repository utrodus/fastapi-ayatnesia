from fastapi import FastAPI
from src.db_helper import test_connections, read_all_surahs, read_all_ayahs_by_surah_id
app = FastAPI()
app.title = (
    "Quran Search API for searching Quranic verses with lexical and semantic features"
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
async def get_all_surahs():
    all_surah = read_all_surahs()
    return all_surah

@app.get("/detail/{surah_id}")
async def get_surah(surah_id: int):
    ayahs = read_all_ayahs_by_surah_id(surah_id)
    return ayahs