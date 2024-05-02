# CDO Global Backend Task

Этот репозиторий содержит решение тестового задания для вакансии бэкенд-разработчика в компании CDO Global. 

## Описание

Этот проект представляет собой реализацию RESTful API с использованием фреймворка FastAPI и языка программирования Python.

**Функциональность API:**
1. **Создание (Create):** Идемпотентный метод для добавления новой записи.
2. **Получение по ID (Get By ID):** Метод для получения данных по уникальному идентификатору.
3. **Получение всех (Get All):** Метод для извлечения данных в формате CSV-файла.
4. **Обновление (Update):** Метод для обновления существующей записи.
5. **Удаление (Delete):** Метод для удаления записи.

**Структура проекта:**
```
fastapi_crud/
│
├── app/
│   ├── __init__.py
│   ├── routers/
│   │   └── __init__.py
│   │   └── items.py
│   ├── database.py
│   ├── exceptions.py
│   ├── main.py
│   ├── models.py
│   ├── schemas.py
│   └── service.py
├── tests/
│   ├── __init__.py
│   ├── test_item.py
│   └── test_export.py
├── README.md
└── requirements.txt
```

### Установка и запуск

1. **Установка зависимостей:** Выполните команду `pip install -r requirements.txt`.
2. **Создание миграций:** Для создания миграций базы данных запустите команду `alembic revision --autogenerate -m "Initial migration"`.
3. **Применение миграций:** Для применения миграций базы данных используйте команду `alembic upgrade head`.
4. **Запуск приложения:** Используйте команду `uvicorn app.main:app --reload`.

### Тестирование

Для запуска тестов используйте pytest: `pytest`.
