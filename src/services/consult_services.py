import requests
from requests.exceptions import HTTPError, Timeout, RequestException
from fastapi.responses import JSONResponse
from logger import get_logger

logger = get_logger(__name__)


async def consult_service(
    url: str,
    method: str = "GET",
    headers: dict = None,
    json_to_send: dict = None,
    params: dict = None,
):
    try:
        logger.info(f"method: {method}")
        logger.info(f"url: {url}")
        method = method.upper()
        if method == "GET":
            response = requests.get(
                url, headers=headers, params=params, timeout=60
            )
        elif method == "POST":
            response = requests.post(
                url, headers=headers, json=json_to_send, timeout=60
            )
        else:
            raise ValueError(f"Método HTTP no soportado: {method}")

        logger.info(f"response: {response.text}")
        response.raise_for_status()
        result = response.json()

        return JSONResponse(result, status_code=response.status_code)

    except HTTPError as http_err:
        logger.error(f"Error en la estructura o contenido de la petición: {http_err}")
        result = {
            "error": f"Petición mal formada o inválida: {str(http_err)}"
        }
        return JSONResponse(
            result, status_code=response.status_code if "response" in locals() else 400
        )

    except Timeout as timeout_err:
        logger.error(f"La solicitud excedió el tiempo de espera: {timeout_err}")
        result = {
            "error": f"Tiempo de espera agotado para conectar con el servicio externo: {str(timeout_err)}"
        }
        return JSONResponse(result, status_code=504)

    except RequestException as req_err:
        logger.error(f"No se pudo conectar con la API: {req_err}")
        result = {
            "error": f"Fallo de conexión con el servicio externo: {str(req_err)}"
        }
        return JSONResponse(result, status_code=502)

    except ValueError as val_err:
        logger.error(f"Error en el método HTTP: {val_err}")
        result = {"error": str(val_err)}
        return JSONResponse(result, status_code=400)









#import requests
#
#from fastapi.responses import JSONResponse
#from logger import get_logger
#from requests.exceptions import RequestException, HTTPError, Timeout
#
#
#logger = get_logger(__name__)
#
#
#async def consult_service(url, json_to_send, headers):
#    try:
#        response = requests.post(url, json=json_to_send, headers=headers, timeout=(60))  # , 30)) # tiempo espera conexion, tiempo espera respuesta
#        logger.info(f"response: {response.text}")
#        response.raise_for_status()
#        result = response.json()
#
#        return JSONResponse(result, status_code=response.status_code)
#
#    except HTTPError as http_err:
#        logger.error(f"Error en la estructura o contenido de la petición: {http_err}")
#        result = {
#            "error": f"Petición mal formada o inválida: {str(http_err)}"
#        }
#        return JSONResponse(result, status_code=response.status_code if 'response' in locals() else 400)
#
#    except Timeout as timeout_err:
#        logger.error(f"La solicitud excedió el tiempo de espera: {timeout_err}")
#        result = {
#            "error": f"Tiempo de espera agotado para conectar con el servicio externo: {str(timeout_err)}"
#        }
#        return JSONResponse(result, status_code=504)  # 504 Gateway Timeout
#
#    except RequestException as req_err:
#        logger.error(f"No se pudo conectar con la API: {req_err}")
#        result = {
#            "error": f"Fallo de conexión con el servicio externo: {str(req_err)}"
#        }
#        return JSONResponse(result, status_code=502)  # 502 Bad Gateway