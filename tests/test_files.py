# test_files.py

from fastapi.testclient import TestClient
from app.main import app
from app.database import get_db
from app import models
import os

client = TestClient(app)

def test_ops_login():
    response = client.post("users/login", json={
        "email": "ops@example.com",
        "password": "ops123"
    })
    assert response.status_code == 200
    assert "access_token" in response.json()

def test_client_signup():
    response = client.post("users/signup", json={
        "role": "client",
        "email": "client11111@example.com",
        "password": "client11111234",
        
    })
    assert response.status_code == 201
    
    

def test_upload_file():
    login = client.post("users/login", json={
        "email": "ops@example.com",
        "password": "ops123"
    })
    token = login.json()["access_token"]

    with open("tests/Presenatation template.pptx", "rb") as file:
        response = client.post(
            "/files/upload",
            files={"file": ("sample.pptx", file, "application/vnd.openxmlformats-officedocument.presentationml.presentation")},
            headers={"Authorization": f"Bearer {token}"}
        )
    assert response.status_code == 200
    assert "file_id" in response.json()

def test_list_files_as_client():
    login = client.post("users/login", json={
        "email": "client@example.com",
        "password": "client123"
    })
    token = login.json()["access_token"]

    response = client.get(
        "/files/list",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    assert isinstance(response.json(), list)

