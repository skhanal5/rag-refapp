from fastapi import FastAPI

from .routes import ingest, health

app = FastAPI()

app.include_router(ingest.router)
app.include_router(health.router)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
