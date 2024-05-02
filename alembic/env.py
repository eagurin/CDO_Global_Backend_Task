# Импортируем необходимые модули из Alembic
from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context

# Импортируем модели из core.models
from app.models import Item
# Если у вас есть другие модели, их также нужно импортировать здесь

# Импортируем модуль базы данных
from app.database import Base

# Используем Alembic для настройки логирования
config = context.config
if config.config_file_name:
    fileConfig(config.config_file_name)

# Получаем метаданные моделей для миграций
target_metadata = Base.metadata

# Функция для запуска миграций в офлайн режиме
def run_migrations_offline():
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()

# Функция для запуска миграций в онлайн режиме
def run_migrations_online():
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()

# Проверяем режим миграций (оффлайн или онлайн)
if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
