from fastapi import APIRouter
from .endpoints import (
    start,
    api_pokemon,
    download,
)

router = APIRouter()


routes_expose = [
    start.router,
    api_pokemon.router,
    download.router,
]

for routes in routes_expose:
    router.include_router(routes, prefix="", tags=["Expose Apis"])
