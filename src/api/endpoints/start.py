from fastapi import Request, APIRouter
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from logger import get_logger


logger = get_logger(__name__)

router = APIRouter()
templates = Jinja2Templates(directory="templates")
logger.info("template: %s", templates)


# Ruta inicial
@router.get("/", response_class=HTMLResponse)
async def mostrar_formulario(request: Request):
    return templates.TemplateResponse("plantilla.html", {"request": request})
