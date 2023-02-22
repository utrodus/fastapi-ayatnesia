from fastapi import FastAPI

app = FastAPI()
app.title = (
    "Quran Search API for searching Quranic verses with lexical and semantic features"
)
app.version = "0.0.1"


@app.get("/")
def hello_world():
    return {"message": "Hello World"}
