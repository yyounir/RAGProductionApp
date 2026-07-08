# Ingest setup
import logging
from fastapi import FastAPI
import inngest
import inngest.fast_api
from inngest.experimental import ai
from dotenv import load_dotenv
import uuid
import os
import datetime

# load the environment variables inside of this .env file
load_dotenv()

inngest_client = inngest.Inngest(
    app_id="rag_app",
    logger = logging.getLogger("uvicorn"),
    is_production=False, # disable production
    serializer=inngest.PydanticSerializer(),
    # Inngest supports pydantic typing
    # Define the types of different variables in this dynamically typed programming language
)

@inngest_client.create_function(
    fn_id="RAG: Ingest PDF",
    trigger=inngest.TriggerEvent(event="rag/ingest_pdf")
)
async def rag_ingest_pdf(ctx: inngest.Context):
    return {"hello": "world"}

# Set up a normal api using fast api
app = FastAPI()

inngest.fast_api.serve(app, inngest_client, [rag_ingest_pdf])