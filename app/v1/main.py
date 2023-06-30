from fastapi import FastAPI

from ..core.models import database
from ..core.settings import engine
from .routers import ad, request, user

database.Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="Worth Trust APIs",
    description="Worth Trust",
    version="1.0.0",
)

app.include_router(
    user.router,
    tags=["User"],
)

app.include_router(
    ad.router,
    tags=["Ad"],
)

app.include_router(
    request.router,
    tags=["Request"],
)
