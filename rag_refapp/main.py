from functools import lru_cache

from fastapi import FastAPI
from rag_refapp.api.routes import health, index, ingest, chat
import uvicorn
from . import config

app = FastAPI()

app.include_router(index.router)
app.include_router(health.router)
app.include_router(ingest.router)
app.include_router(chat.router)


@lru_cache
def get_settings():
    return config.Settings


if __name__ == "__main__":

    # Load settings here

    uvicorn.run("rag_refapp.main:app", host="0.0.0.0", port=8000, reload=True)
