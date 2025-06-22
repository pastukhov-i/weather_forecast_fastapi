from typing import Any

from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession


class SessionContextManager:
    def __init__(self, async_session: async_sessionmaker[AsyncSession]) -> None:
        self._async_session = async_session
        self._session: AsyncSession | None = None

    async def __aenter__(self) -> AsyncSession:
        self._session = self._async_session()
        return self._session

    async def __aexit__(
        self, exc_type: type[Exception], exc_val: Exception, exc_tb: Any
    ) -> None:
        if not self._session:
            return

        try:
            if exc_val:
                await self._session.rollback()
                raise exc_val
        finally:
            if self._session:
                await self._session.close()
                self._session = None
