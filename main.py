import uvicorn
from logger import get_logger
from config import Settings


settings = Settings()

logger = get_logger(__name__, settings.LOG_LEVEL)

logger.info("ENV: %s", settings.ENV)

PORT = settings.PORT
HOST = settings.HOST

logger.info("PORT: %s", settings.PORT)
logger.info("HOST: %s", settings.HOST)


def main():
    uvicorn.run(
        "src.app:app",
        host=str(HOST),
        port=int(PORT),
        reload=True
    )


if __name__ == "__main__":
    main()
