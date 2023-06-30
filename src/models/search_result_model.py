from pydantic import BaseModel

class SearchResult(BaseModel):
    execution_time: float
    results: list