from configparser import NoSectionError
from logging.config import fileConfig
from typing import Any

from alembic import context
from sqlalchemy import Connection, engine_from_config, pool

from open_gallery.api.settings import APISettings
from open_gallery.persistence.tables.base import mapper_registry
from open_gallery.persistence.tables.users import users

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata
tables = [users]
target_metadata = mapper_registry.metadata

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.
conf = config.get_section(config.config_ini_section, {})
if not conf:
    msg = "No conf found"
    raise NoSectionError(msg)

settings = APISettings().database

conf["sqlalchemy.url"] = str(settings.dsn).replace("postgresql+asyncpg://", "postgresql://")
conf["version_table_schema"] = settings.schema


def include_name(name: str | None, type_: Any, _: Any) -> bool:  # noqa: ANN401
    if type_ == "schema":
        return name == settings.schema
    return True


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    context.configure(
        url=str(settings.dsn),
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        include_name=include_name,
        version_table_schema=settings.schema,
    )

    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection: Connection) -> None:
    if settings.schema != "public":
        extra_config = {
            "version_table_schema": settings.schema,
            "include_schemas": True,
            "include_name": include_name,
        }
    else:
        extra_config = {}
    context.configure(
        connection=connection,
        target_metadata=target_metadata,
        **extra_config,  # type: ignore[arg-type]
    )
    with context.begin_transaction():
        context.execute(f"set search_path to {settings.schema}")
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """

    _db_dsn = context.get_x_argument(as_dictionary=True).get("DB_DSN")
    conf["sqlalchemy.url"] = _db_dsn or str(settings.dsn).replace("postgresql+asyncpg://", "postgresql://")
    connectable = engine_from_config(
        conf,
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )
    with connectable.connect() as connection:
        do_run_migrations(connection)


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
