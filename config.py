from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # Enviroment and server configuration
    APP_NAME: str = "Fast Api project"
    ENV: str = "Local"
    HOST: str = "localhost"
    PORT: int = 8005
    LOG_LEVEL: str = "INFO"
    BASE_PATH: str = "/api"
    SERVICE_VERSION: str = "2.0.0"

    # Authentication and security
    SWAGGER_USER: str = "admin"
    SWAGGER_PASS: str = "admin_password"

    # Database Configuration
    MONGO_URI: str = "mongodb://localhost:27017"
    MONGO_DB: str = "APIS"
    MONGO_USERS_COLLECTION: str = "users"
    MONGO_POKEMON_COLLECTION: str = "pokemon"

    # External API Configuration
    POKEMON_API_URL: str = "https://pokeapi.co/api/v2/pokemon/ditto"

    model_config = SettingsConfigDict(env_file=".env", extra="allow")
