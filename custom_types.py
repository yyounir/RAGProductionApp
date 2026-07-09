import pydantic

class RAGChunkAndSrc(pydantic.BaseModel):
    chunks: list[str]
    source_id: str = None
    # The result after we chunk the and get the source for a particular PDF document

# Result after we upsert a document
class RAGUpsertResult(pydantic.BaseModel):
    ingested: int

class RAGSearchResult(pydantic.BaseModel):
    contexts: list[str]
    sources: list[str]

class RAGQueryResult(pydantic.BaseModel):
    answer: str
    sources: list[str]
    num_contexts: int