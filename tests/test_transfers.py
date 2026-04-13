
from fastapi.testclient import TestClient
from app.main import app
from app.storage import transfers_db, idempotency_index

client = TestClient(app)


def setup_function():
    transfers_db.clear()
    idempotency_index.clear()


def test_create_transfer_happy_path():
    payload = {
        "from_account_id": "ACC-001",
        "to_alias": "alias.destino",
        "amount": 250.0,
        "currency": "ARS",
        "idempotency_key": "IDEMP-001",
    }

    response = client.post("/transfers", json=payload)

    assert response.status_code == 202
    body = response.json()
    assert body["state"] == "PENDING"
    assert body["amount"] == 250.0
    assert body["currency"] == "ARS"
    assert body["idempotency_key"] == "IDEMP-001"
    assert body["transfer_id"].startswith("TRF-")


def test_create_transfer_rejects_invalid_currency():
    payload = {
        "from_account_id": "ACC-001",
        "to_alias": "alias.destino",
        "amount": 250.0,
        "currency": "USD",
        "idempotency_key": "IDEMP-002",
    }

    response = client.post("/transfers", json=payload)

    assert response.status_code == 400
    assert response.json()["detail"]["error_code"] == "UNSUPPORTED_CURRENCY"


def test_create_transfer_rejects_negative_amount():
    payload = {
        "from_account_id": "ACC-001",
        "to_alias": "alias.destino",
        "amount": -10.0,
        "currency": "ARS",
        "idempotency_key": "IDEMP-003",
    }

    response = client.post("/transfers", json=payload)

    assert response.status_code == 422


def test_create_transfer_is_idempotent():
    payload = {
        "from_account_id": "ACC-001",
        "to_alias": "alias.destino",
        "amount": 250.0,
        "currency": "ARS",
        "idempotency_key": "IDEMP-004",
    }

    response_1 = client.post("/transfers", json=payload)
    response_2 = client.post("/transfers", json=payload)

    assert response_1.status_code == 202
    assert response_2.status_code == 202
    assert response_1.json()["transfer_id"] == response_2.json()["transfer_id"]


def test_get_transfer_by_id():
    payload = {
        "from_account_id": "ACC-001",
        "to_alias": "alias.destino",
        "amount": 250.0,
        "currency": "ARS",
        "idempotency_key": "IDEMP-005",
    }

    created = client.post("/transfers", json=payload).json()
    transfer_id = created["transfer_id"]

    response = client.get(f"/transfers/{transfer_id}")

    assert response.status_code == 200
    assert response.json()["transfer_id"] == transfer_id


def test_get_transfer_not_found():
    response = client.get("/transfers/TRF-UNKNOWN")

    assert response.status_code == 404
    assert response.json()["detail"]["error_code"] == "TRANSFER_NOT_FOUND"
