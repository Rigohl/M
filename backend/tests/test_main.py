import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

# Pruebas para el endpoint de creación de canciones
def test_create_song():
    response = client.post("/create-song", json={
        "title": "Mi Corrido",
        "artist": "Juan Pérez",
        "genre": "Regional Mexicano"
    })
    assert response.status_code == 200
    assert response.json() == {
        "message": "Canción creada exitosamente",
        "data": {
            "title": "Mi Corrido",
            "artist": "Juan Pérez",
            "genre": "Regional Mexicano"
        }
    }

# Pruebas para el registro de usuarios
def test_register_user():
    response = client.post("/register-user", json={
        "email": "test@example.com",
        "password": "securepassword"
    })
    assert response.status_code == 200
    assert "user" in response.json()

# Pruebas para el inicio de sesión
def test_login_user():
    response = client.post("/login-user", json={
        "email": "test@example.com",
        "password": "securepassword"
    })
    assert response.status_code == 200
    assert "user" in response.json()
