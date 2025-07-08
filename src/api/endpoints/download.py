from fastapi.responses import FileResponse
from fastapi import APIRouter
from logger import get_logger


router = APIRouter()
logger = get_logger(__name__)


# Ruta para descargar el archivo xlsx
@router.get("/descargar-xlsx")
async def descargar_xlsx():
    filename = "C:/Users/gonza/Dropbox/PC/Documents/FastApi/downloads/pokemon.xlsx"
    return FileResponse(
        filename,
        filename=filename,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
