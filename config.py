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

    # External API Configuration
    BELVO_API_URL: str = "https://sandbox.belvo.com/api/transactions/?page_size=100&link=acc5ba41-e462-4156-a7c7-382a725e76b6"
    BELVO_KEY: str = "Basic MmIxNWJhODgtYTE4NS00ODU1LWEyMDEtNmRmMWZhZDVmNTYwOmhZbVRjMS1FdlNiQFpzcGtHbU5OVVRVI2VlYVN5SWJITy1MZjRQUVBHWkE4S2ZtVnRCSGlEWWMwc2gwZDJQKnI="
    POKEMON_API_URL: str = "https://pokeapi.co/api/v2/pokemon/ditto"

    model_config = SettingsConfigDict(env_file=".env", extra="allow")
