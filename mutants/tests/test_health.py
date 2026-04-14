
from fastapi.testclient import TestClient
from lib_core.utils.app.main import app
import pytest

client = TestClient(app)

@pytest.mark.payments
class TestPayments:
    
    def test_healthcheck_returns_ok(self):
        response = client.get("/health")
    
        assert response.status_code == 200
        assert response.json() == {"status": "ok"}
