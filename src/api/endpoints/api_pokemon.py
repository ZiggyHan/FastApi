from fastapi import Request, Form, APIRouter, HTTPException, status
from fastapi.templating import Jinja2Templates
from src.schemas.login_form import LoginForm
from src.database.mongodb import MongoDBConnection
from config import Settings
from logger import get_logger
from src.services.consult_services import consult_service

import pandas as pd
import json


router = APIRouter()
templates = Jinja2Templates(directory="templates")
settings = Settings()
logger = get_logger(__name__)


# Ruta para manejar los datos del formulario
@router.post("/names_pokemon")
async def api_pokemon_names(
    request: Request,
    email: str = Form(...),
    password: str = Form(...)
):
    # Validación del form dada por el front
    form = LoginForm(email=email, password=password)

    # Conexión MongoDB
    mongo_conn = MongoDBConnection(settings.MONGO_URI)
    collection = mongo_conn.get_collection(settings.MONGO_DB,
                                           settings.MONGO_USERS_COLLECTION)  # Ajusta tus nombres
    logger.info(f"MONGO_URI: {settings.MONGO_URI}")
    logger.info(f"MONGO_DB: {settings.MONGO_DB}")
    logger.info(f"MONGO_USERS_COLLECTION: {settings.MONGO_USERS_COLLECTION}")

    # Busca en MongoDB
    user = collection.find_one({
        "email": form.email,
        "password": form.password  # En producción DEBES usar hash, no texto plano
    })

    if not user:
        return HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Correo o contraseña incorrectos"
        )

    external_urlApi = settings.POKEMON_API_URL
    logger.info(f"external_urlApi: {settings.POKEMON_API_URL}")
    method = "get"
    logger.info(f"method: {method}")

    # response = requests.get(external_urlApi)
    # response_dict = response.json()
    response_dict = await consult_service(url=external_urlApi, method=method)
    logger.info(f"response_dict: {response_dict}")

    # Decodifica el cuerpo del JSONResponse
    data = json.loads(response_dict.body)
    pokemon_list = data["results"]
    logger.info(f"pokemon_list: {pokemon_list}")

    # Conversión directa
    df = pd.DataFrame(pokemon_list)

    df.to_excel("C:/Users/gonza/Dropbox/PC/Documents/FastApi/downloads/pokemon.xlsx", index=False)
    logger.info("se transformo con exito a archivo xlsx")

    # Este es el resultado de las entradas de una categoria en formato xlsx
    return templates.TemplateResponse("descargar.html", {"request": request})
