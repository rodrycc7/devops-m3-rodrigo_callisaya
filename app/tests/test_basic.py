import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest
from main import app, reset_inventory


@pytest.fixture
def client():
    app.config["TESTING"] = True
    reset_inventory()
    with app.test_client() as c:
        yield c


def test_health(client):
    resp = client.get("/health")
    assert resp.status_code == 200
    assert resp.get_json()["status"] == "ok"


def test_lista_inicial_de_juegos(client):
    games = client.get("/games").get_json()
    assert len(games) == 4
    assert any("Mario Kart" in g["title"] for g in games)


def test_filtrar_por_genero(client):
    games = client.get("/games?genre=carreras").get_json()
    assert len(games) == 1
    assert games[0]["title"] == "Mario Kart 8 Deluxe"


def test_crear_juego(client):
    resp = client.post("/games", json={
        "title": "Metroid Dread", "genre": "Acción", "price": 49.99, "stock": 6})
    assert resp.status_code == 201
    assert client.get(f"/games/{resp.get_json()['id']}").status_code == 200


def test_crear_juego_sin_titulo(client):
    resp = client.post("/games", json={"genre": "Acción", "price": 10, "stock": 1})
    assert resp.status_code == 400


def test_actualizar_stock(client):
    resp = client.put("/games/1/stock", json={"stock": 20})
    assert resp.status_code == 200
    assert resp.get_json()["stock"] == 20


def test_eliminar_juego(client):
    assert client.delete("/games/2").status_code == 204
    assert client.get("/games/2").status_code == 404
