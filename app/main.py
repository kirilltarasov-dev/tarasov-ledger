from fastapi import FastAPI
from app.api import upload
from app.db.database import init_db
from contextlib import asynccontextmanager


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield


app = FastAPI(lifespan=lifespan)

app.include_router(upload.router, prefix="/upload", tags=["Upload"])


@app.get("/health")
def health_check():
    return {"status": "ok"}
