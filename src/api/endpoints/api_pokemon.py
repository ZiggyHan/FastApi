from fastapi import FastAPI, Request, Form, APIRouter, HTTPException, status
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.responses import FileResponse
import os
from src.schemas.login_form import LoginForm
from src.database.mongodb import MongoDBConnection
from config import Settings
from logger import get_logger


import requests
import pandas as pd
import json
import subprocess

#UPLOAD_FOLDER = os.path.dirname(os.path.abspath(__file__)) + '/uploads'
DOWNLOAD_FOLDER = "downloads"

router = APIRouter()
templates = Jinja2Templates(directory="templates")
settings = Settings()
logger = get_logger(__name__)


# Función para exportar DataFrame a un archivo xlsx
def export_to_excel(df, filename):
    filepath = os.path.join(DOWNLOAD_FOLDER, filename)
    df.to_excel(filepath, index=False)
    return filepath


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
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Correo o contraseña incorrectos"
        )

    # Aquí ya tienes datos validados
    return {"message": "Inicio de sesión exitoso", "user": {"email": user["email"]}}


    form_data = await request.form()
    email = form_data.get("email")
    password = form_data.get("password")
    if email == "alexi.numat@gmail.com" and password == "12345":
        ##### CONEXION #####
        # Transaction
        url2 = "https://sandbox.belvo.com/api/transactions/?page_size=100&link=acc5ba41-e462-4156-a7c7-382a725e76b6"

        headers = {"accept": "application/json",
                   "authorization": "Basic MmIxNWJhODgtYTE4NS00ODU1LWEyMDEtNmRmMWZhZDVmNTYwOmhZbVRjMS1FdlNiQFpzcGtHbU5OVVRVI2VlYVN5SWJITy1MZjRQUVBHWkE4S2ZtVnRCSGlEWWMwc2gwZDJQKnI="
                   }

        def resources(URL, HEADERS):
            response = requests.get(URL, headers=HEADERS)
            return response

        list_url = [url2]
        list_request_response = []
        for i in list_url:
            list_request_response.append(resources(i, headers))

        # TRANSFORMACION
        # Verificar si la solicitud fue exitosa (código de respuesta 200)
        list_df_principal = []
        for i in list_request_response:
            if i.status_code == 200:
                # Convertir el contenido JSON de la respuesta en un DataFrame
                list_df_principal.append(pd.DataFrame(i.json()))
                # Imprimir el DataFrame o realizar cualquier otra acción que desees
                #print(df)
            else:
                # Si la solicitud no fue exitosa, imprimir el mensaje de error
                print(f"Error: {i.status_code} - {i.text}")
                # Procesar los datos como desees
                return templates.TemplateResponse("index.html", {"request": request})
            
        df_transfer = pd.DataFrame(list(list_df_principal[0]['results']))
        transfer1 = df_transfer.filter(['id', 'category', 'type', 'amount', 'status', 'balance', 'reference'])
        df_transfer2 = pd.DataFrame(list(df_transfer['account']))
        transfer2 = df_transfer2.filter(['id', 'name', 'type', 'category', 'bank_product_id', 'internal_identification'])
    
        transfer_completo = pd.concat([transfer1, transfer2], axis=1)
    
        transfer_completo.columns = ['id', 'category', 'type_pago', 'Amount', 'status_pago', 'balance', 'reference', 
                                     'id_producto', 'producto', 'type2', 'category2', 'bank_product_id2', 'internal_identification2']
        
        list_usuarios = list(transfer_completo['id'])

        # Entradas y Salidas
        transfer_completo_entradas = transfer_completo[transfer_completo['type_pago'] == 'INFLOW']
        transfer_completo_salidas = transfer_completo[transfer_completo['type_pago'] == 'OUTFLOW']

        # Entradas y salidas ordenadas por categoría
        list_entradas = list(transfer_completo_entradas['category'].unique())
        list_salidas = list(transfer_completo_salidas['category'].unique())

        list_df_categoy_entradas = []
        list_df_categoy_salidas = []
        for i in range(len(list_entradas)):
            list_df_categoy_entradas.append(transfer_completo_entradas[transfer_completo_entradas['category'] == list_entradas[i]].filter(['id', 'category', 'Amount']))
            list_df_categoy_salidas.append(transfer_completo_salidas[transfer_completo_salidas['category'] == list_salidas[i]].filter(['id', 'category', 'Amount']))
        
        # Exportar el DataFrame a un archivo Excel (la ruta para que jale en su ordenador hay que cambiarla)
        # Esto se puede optimizar con la libreria os (para hacer la ruta dinamica)
        list_df_categoy_salidas[0].to_excel("C:/Users/gonza/Dropbox/PC/Documents/FastApi/downloads/archivo.xlsx", index=False)

        # Este es el resultado de las entradas de una categoria en formato xlsx
        return templates.TemplateResponse("descargar.html", {"request": request})
    #{
     #           "Lista Usuarios": list_usuarios[:]
      #      }
    #templates.TemplateResponse("descargar.html", {"request": request})
        # Si en lugar d
        #{
                #"Lista Usuarios": list_usuarios[:]
            #}

    else:
        return "Credenciales incorrectas"