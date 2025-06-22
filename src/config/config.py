from functools import lru_cache

from dotenv import load_dotenv
from pydantic import BaseModel
from pydantic import Field
from pydantic_settings import BaseSettings


load_dotenv()


class WeatherAPIConfig(BaseSettings):
    weather_api_url: str
    openweather_api_key: str


class DatabaseConfig(BaseSettings):
    password: str = Field(alias="POSTGRES_PASSWORD")
    host: str = Field(alias="POSTGRES_HOST")
    user: str = Field(alias="POSTGRES_USER")
    port: int = Field(alias="POSTGRES_PORT")
    name: str = Field(alias="POSTGRES_NAME")


class MainConfig(BaseModel):
    weather_api: WeatherAPIConfig = WeatherAPIConfig()
    database: DatabaseConfig = DatabaseConfig()


@lru_cache
def get_config() -> MainConfig:
    return MainConfig()
