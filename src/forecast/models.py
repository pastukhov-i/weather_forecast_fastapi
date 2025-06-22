from datetime import date

from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.sql.sqltypes import String

from src.models import Base


class Forecast(Base):
    __tablename__ = "forecasts"

    id: Mapped[int] = mapped_column(primary_key=True)
    city: Mapped[str] = mapped_column(String(100))
    date: Mapped[date]
    min_temperature: Mapped[float]
    max_temperature: Mapped[float]
