# tests/test_item.py

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_create_item():
    data = {"name": "Тестовый предмет", "description": "Это тестовый предмет"}
    response = client.post("/items/", json=data)
    assert response.status_code == 201
    assert response.json()["name"] == "Тестовый предмет"
    assert response.json()["description"] == "Это тестовый предмет"


def test_read_item():
    response = client.post(
        "/items/",
        json={
            "name": "Тестовый предмет",
            "description": "Это тестовый предмет",
        },
    )
    item_id = response.json()["id"]
    response = client.get(f"/items/{item_id}")
    assert response.status_code == 200
    assert response.json()["name"] == "Тестовый предмет"
    assert response.json()["description"] == "Это тестовый предмет"


def test_update_item():
    # Создание нового элемента
    create_response = client.post(
        "/items/",
        json={
            "name": "Тестовый предмет",
            "description": "Это тестовый предмет",
        },
    )
    assert create_response.status_code == 201
    item_id = create_response.json()["id"]

    # Обновление элемента
    update_data = {
        "name": "Обновленное название предмета",
        "description": "Это тестовый предмет",
    }
    update_response = client.put(f"/items/{item_id}", json=update_data)
    assert update_response.status_code == 200
    assert update_response.json()["name"] == "Обновленное название предмета"
    assert update_response.json()["description"] == "Это тестовый предмет"


def test_delete_item():
    response = client.post(
        "/items/",
        json={
            "name": "Тестовый предмет",
            "description": "Это тестовый предмет",
        },
    )
    item_id = response.json()["id"]
    response = client.delete(f"/items/{item_id}")
    assert response.status_code == 204
    response = client.get(f"/items/{item_id}")
    assert response.status_code == 404
