from fastapi.testclient import TestClient
import sys
import os
import pytest

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from main import app

client = TestClient(app)

def test_create_trade():
    response = client.post("/api/v1/trade/request", json={
        "initiator_trainer_id": 1,
        "receiver_trainer_id": 2,
        "initiator_pokemon_id": 3,
        "receiver_pokemon_id": 4,
        "condition": {
            "required_type": "Fire",
            "min_level": 10
        }
    })
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "pending"

def test_accept_trade():
    # First create a trade
    response = client.post("/api/v1/trade/request", json={
        "initiator_trainer_id": 1,
        "receiver_trainer_id": 2,
        "initiator_pokemon_id": 3,
        "receiver_pokemon_id": 4,
        "condition": {
            "required_type": "Fire",
            "min_level": 10
        }
    })
    trade_id = response.json()["id"]

    # Now accept the trade
    response = client.post(f"/api/v1/trade/accept/{trade_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "accepted"

def test_reject_trade():
    # First create a trade
    response = client.post("/api/v1/trade/request", json={
        "initiator_trainer_id": 1,
        "receiver_trainer_id": 2,
        "initiator_pokemon_id": 3,
        "receiver_pokemon_id": 4,
        "condition": {
            "required_type": "Fire",
            "min_level": 10
        }
    })
    trade_id = response.json()["id"]

    # Now reject the trade
    response = client.post(f"/api/v1/trade/reject/{trade_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "rejected"

def test_cancel_trade():
    # First create a trade
    response = client.post("/api/v1/trade/request", json={
        "initiator_trainer_id": 1,
        "receiver_trainer_id": 2,
        "initiator_pokemon_id": 3,
        "receiver_pokemon_id": 4,
        "condition": {
            "required_type": "Fire",
            "min_level": 10
        }
    })
    trade_id = response.json()["id"]

    # Now cancel the trade
    response = client.post(f"/api/v1/trade/cancel/{trade_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "cancelled"

def test_trade_history():
    response = client.get("/api/v1/trade/history/1")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
