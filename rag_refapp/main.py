from fastapi import FastAPI
from rag_refapp.api.routes import health, index
import uvicorn

app = FastAPI()

app.include_router(index.router)
app.include_router(health.router)

if __name__ == "__main__":
    uvicorn.run("rag_refapp.main:app", host="0.0.0.0", port=8000)
