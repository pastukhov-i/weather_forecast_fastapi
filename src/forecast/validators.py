import datetime

from fastapi import HTTPException
from starlette import status


def validate_date_string(date: str) -> str:
    try:
        datetime.datetime.strptime(date, "%d.%m.%Y")
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Неверный формат даты. Пример: DD.MM.YYYY",
        )

    return date


def validate_date_not_in_past(date: str) -> str:
    if datetime.datetime.strptime(date, "%d.%m.%Y") < datetime.datetime.today():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Дата не может быть в прошлом",
        )

    return date


def validate_date_is_less_than_3_days_away(date: str) -> str:
    if datetime.datetime.strptime(
        date, "%d.%m.%Y"
    ) - datetime.datetime.today() > datetime.timedelta(days=3):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Дата не может больше 3 дней от сегодняшнего дня",
        )

    return date


def validate_date(date: str) -> str:
    validate_date_string(date)
    validate_date_not_in_past(date)
    validate_date_is_less_than_3_days_away(date)

    return date
