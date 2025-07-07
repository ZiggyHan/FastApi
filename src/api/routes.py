from fastapi import APIRouter
from .endpoints import (
    start,
    api_pokemon
)

router = APIRouter()


routes_expose = [
    start.router,
    api_pokemon.router
]

for routes in routes_expose:
    router.include_router(routes, prefix="", tags=["Exppose Apis"])
