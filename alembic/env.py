import os
from logging.config import fileConfig
from alembic import context
from sqlalchemy import engine_from_config, pool
from dotenv import load_dotenv

load_dotenv()
config = context.config
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

from database.db import metadata  # noqa: E402

target_metadata = metadata


def get_url():
    return os.getenv('DATABASE_URL', 'sqlite:///family_finance.db')


def run_migrations_offline():
    url = get_url()
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={'paramstyle': 'named'},
        render_as_batch=url.startswith('sqlite'),
    )
    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    configuration = config.get_section(config.config_ini_section) or {}
    url = get_url()
    configuration['sqlalchemy.url'] = url
    connectable = engine_from_config(configuration, prefix='sqlalchemy.', poolclass=pool.NullPool)
    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata, render_as_batch=url.startswith('sqlite'))
        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
