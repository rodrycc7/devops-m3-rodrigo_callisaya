"""
Inventario de juegos de Nintendo Switch - API REST (Flask)
Autor: Rodrigo Callisaya Cameo
Curso DevOps - Módulo 3 (Educomser)
"""
import os
from flask import Flask, jsonify, request

app = Flask(__name__)

# Almacenamiento en memoria con algunos juegos de ejemplo
_games = {}
_next_id = 1


def _add_game(title, genre, price, stock):
    global _next_id
    game = {"id": _next_id, "title": title, "genre": genre,
            "price": price, "stock": stock}
    _games[_next_id] = game
    _next_id += 1
    return game


def reset_inventory():
    """Restaura el inventario inicial (usado también por las pruebas)."""
    global _next_id
    _games.clear()
    _next_id = 1
    _add_game("The Legend of Zelda: Tears of the Kingdom", "Aventura", 69.99, 8)
    _add_game("Mario Kart 8 Deluxe", "Carreras", 59.99, 15)
    _add_game("Animal Crossing: New Horizons", "Simulación", 59.99, 10)
    _add_game("Super Smash Bros. Ultimate", "Pelea", 59.99, 5)


reset_inventory()


@app.get("/health")
def health():
    return jsonify(status="ok", servicio="switch-inventory"), 200


@app.get("/games")
def list_games():
    genre = request.args.get("genre")
    games = list(_games.values())
    if genre:
        games = [g for g in games if g["genre"].lower() == genre.lower()]
    return jsonify(games), 200


@app.get("/games/<int:game_id>")
def get_game(game_id):
    game = _games.get(game_id)
    if not game:
        return jsonify(error="Juego no encontrado"), 404
    return jsonify(game), 200


@app.post("/games")
def create_game():
    data = request.get_json(silent=True) or {}
    title = str(data.get("title", "")).strip()
    genre = str(data.get("genre", "")).strip()
    try:
        price = float(data.get("price", 0))
        stock = int(data.get("stock", 0))
    except (TypeError, ValueError):
        return jsonify(error="'price' y 'stock' deben ser numéricos"), 400
    if not title or not genre:
        return jsonify(error="Los campos 'title' y 'genre' son obligatorios"), 400
    if price < 0 or stock < 0:
        return jsonify(error="'price' y 'stock' no pueden ser negativos"), 400
    return jsonify(_add_game(title, genre, price, stock)), 201


@app.put("/games/<int:game_id>/stock")
def update_stock(game_id):
    game = _games.get(game_id)
    if not game:
        return jsonify(error="Juego no encontrado"), 404
    data = request.get_json(silent=True) or {}
    try:
        stock = int(data["stock"])
    except (KeyError, TypeError, ValueError):
        return jsonify(error="Se requiere 'stock' numérico"), 400
    if stock < 0:
        return jsonify(error="'stock' no puede ser negativo"), 400
    game["stock"] = stock
    return jsonify(game), 200


@app.delete("/games/<int:game_id>")
def delete_game(game_id):
    if _games.pop(game_id, None) is None:
        return jsonify(error="Juego no encontrado"), 404
    return "", 204


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", "8080")))
