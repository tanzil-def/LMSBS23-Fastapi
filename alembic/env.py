from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context

import sys, os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

# Import Base and all models
from app.db.base import Base  # Base.metadata
from app.models.user import User
from app.models.book import Book
from app.models.category import Category
from app.models.booking import Booking  # যেটা foreign key use করছে

# this is the Alembic Config object
config = context.config
fileConfig(config.config_file_name)

target_metadata = Base.metadata

def run_migrations_online():
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix='sqlalchemy.',
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True
        )

        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    raise Exception("Offline mode not configured")
else:
    run_migrations_online()
