from dependency_injector import providers
from dependency_injector.containers import DeclarativeContainer
from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine

from src.config.config import get_config
from src.database import SessionContextManager
from src.forecast.container import ForecastContainer


class DatabaseContainer(DeclarativeContainer):
    config = get_config()

    db_url = f"postgresql+asyncpg://{config.database.user}:{config.database.password}@{config.database.host}:{config.database.port}/{config.database.name}"

    engine = providers.Singleton(provides=create_async_engine, url=db_url)

    async_session = providers.Singleton(
        provides=async_sessionmaker, bind=engine, expire_on_commit=False
    )

    session_manager = providers.Factory(
        provides=SessionContextManager, async_session=async_session
    )


class RootContainer(DeclarativeContainer):
    database_container = providers.Container(container_cls=DatabaseContainer)

    forecast_container = providers.Container(
        container_cls=ForecastContainer,
        session_manager=database_container.session_manager,
    )
