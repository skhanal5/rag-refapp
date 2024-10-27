from fastapi import FastAPI
from app.api.routes import health, index, ingest, chat
import uvicorn

app = FastAPI()

app.include_router(index.router)
app.include_router(health.router)
app.include_router(ingest.router)
app.include_router(chat.router)


if __name__ == "__main__":
    uvicorn.run("rag_refapp.main:app", host="0.0.0.0", port=8000, reload=True)
