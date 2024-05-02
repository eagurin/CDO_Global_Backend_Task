# tests/test_export.py

import csv
from io import StringIO

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.database import Base
from app.models import Item

SQLALCHEMY_DATABASE_URL = "sqlite:///./app.db"


# Фикстура для создания тестового клиента
@pytest.fixture
def client():
    from app.main import app

    with TestClient(app) as client:
        yield client


# Фикстура для создания сеанса базы данных для тестирования
@pytest.fixture
def db_session():
    engine = create_engine(
        SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
    )
    TestingSessionLocal = sessionmaker(
        autocommit=False, autoflush=False, bind=engine
    )
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


# Тест для чтения всех элементов в формате CSV
def test_read_all_items_as_csv(client, db_session):
    # Вставка тестовых данных в базу данных
    items = [
        Item(name="Тестовый элемент 1", description="Это тестовый элемент 1"),
        Item(name="Тестовый элемент 2", description="Это тестовый элемент 2"),
    ]
    db_session.add_all(items)
    db_session.commit()

    # Получение элементов в формате CSV через API
    response = client.get("/items/all")
    assert response.status_code == 200
    assert "text/csv" in response.headers["Content-Type"]
    assert (
        response.headers["Content-Disposition"]
        == "attachment; filename=items.csv"
    )

    # Проверка содержимого CSV
    csv_data = response.text
    csv_reader = csv.reader(StringIO(csv_data))
    headers = next(csv_reader)
    assert headers == ["id", "name", "description"]

    # Получение элементов из базы данных напрямую
    db_items = db_session.query(Item).all()

    # Сравнение содержимого CSV с элементами из базы данных
    for db_item, csv_row in zip(db_items, csv_reader):
        assert csv_row[0] == str(db_item.id)
        assert csv_row[1] == db_item.name
        assert csv_row[2] == db_item.description
