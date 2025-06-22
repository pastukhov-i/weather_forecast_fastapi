import datetime

from pydantic import BaseModel
from pydantic import ConfigDict
from pydantic import field_serializer
from pydantic import field_validator
from pydantic import ValidationError


class CurrentBodyAPIResponse(BaseModel):
    last_updated_epoch: int
    temp_c: float


class LocationBodyAPIResponse(BaseModel):
    tz_id: str


class BaseWeatherAPIResponse(BaseModel):
    location: LocationBodyAPIResponse


class CurrentWeatherAPIResponse(BaseWeatherAPIResponse):
    current: CurrentBodyAPIResponse


class DayBodyAPIResponse(BaseModel):
    maxtemp_c: float
    mintemp_c: float


class ForecastDayBodyResponse(BaseModel):
    date_epoch: int
    day: DayBodyAPIResponse


class ForecastBodyAPIResponse(BaseModel):
    forecastday: list[ForecastDayBodyResponse]


class ForecastWeatherAPIResponse(BaseWeatherAPIResponse):
    forecast: ForecastBodyAPIResponse


class CurrentForecastSchema(BaseModel):
    temperature: float
    local_time: str


class ForecastCreateSchema(BaseModel):
    city: str
    date: datetime.date
    min_temperature: float
    max_temperature: float

    @field_validator("date", mode="before")
    @classmethod
    def format_date(cls, raw_data: str) -> datetime.date:
        try:
            return datetime.datetime.strptime(raw_data, "%d.%m.%Y")
        except ValueError:
            raise ValidationError


class ForecastListSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    city: str
    date: datetime.date
    min_temperature: float
    max_temperature: float

    @field_serializer("date")
    def serialize_date(self, value: datetime.date) -> str:
        try:
            return value.strftime("%d.%m.%Y")
        except ValueError:
            raise ValidationError
