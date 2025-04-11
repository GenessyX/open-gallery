from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from open_gallery.persistence.settings import DatabaseSettings


class Database:
    def __init__(self, settings: DatabaseSettings) -> None:
        self._settings = settings

        self._engine = create_async_engine(
            url=str(settings.dsn),
            echo=False,
            echo_pool=False,
            pool_pre_ping=settings.pool_pre_ping,
            pool_recycle=int(settings.pool_recycle.total_seconds()),
            max_overflow=settings.max_overflow,
            connect_args={"server_settings": {"search_path": settings.schema}},
        )

        self._session_maker = async_sessionmaker(
            bind=self._engine,
            autocommit=False,
            autoflush=False,
            expire_on_commit=False,
        )

    def get_async_session(self) -> AsyncSession:
        return self._session_maker()
