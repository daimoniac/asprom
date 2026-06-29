import os
from logging.config import fileConfig

from sqlalchemy import engine_from_config, pool

from alembic import context

config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = None


def _database_url() -> str:
    if url := os.environ.get("ASPROM_DB_URL"):
        return url
    host = os.environ.get("ASPROM_TEST_DB_HOST", os.environ.get("MYSQL_HOST", "127.0.0.1"))
    port = os.environ.get("ASPROM_TEST_DB_PORT", os.environ.get("MYSQL_PORT", "3306"))
    user = os.environ.get("ASPROM_TEST_DB_USER", os.environ.get("MYSQL_USER", "asprom"))
    password = os.environ.get("ASPROM_TEST_DB_PASSWORD", os.environ.get("MYSQL_PASSWORD", "asprom"))
    database = os.environ.get("ASPROM_TEST_DB_NAME", os.environ.get("MYSQL_DATABASE", "asprom"))
    return f"mysql+mysqldb://{user}:{password}@{host}:{port}/{database}"


def run_migrations_offline() -> None:
    context.configure(
        url=_database_url(),
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    configuration = config.get_section(config.config_ini_section, {})
    configuration["sqlalchemy.url"] = _database_url()
    connectable = engine_from_config(
        configuration,
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
