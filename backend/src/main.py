import os
from orm.database import get_db
from utils.tools import create_test_data

if os.getenv("HADES_TESTING", "False") == "True":
    create_test_data(next(get_db()))

from fastapi import FastAPI

from routers import admin, image
from routers.hades.api import router as hades_router

app = FastAPI()
app.include_router(admin.router)
app.include_router(hades_router)
app.include_router(image.router)


@app.get("/health")
async def connectionStatus() -> bool:
    """
    Health Check API Endpoint
    """
    return True
