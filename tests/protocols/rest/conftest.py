"""
rest-specific fixtures
"""

import pytest
import logging
from fastapi.testclient import TestClient

from lib_core.utils.app.main import app
from lib_core.utils.apis.rest.payments_api import PaymentsAPI

from lib_core.utils.app.storage import transfers_db, idempotency_index

from hypothesis import settings
from hypothesis import HealthCheck


settings.register_profile(
    "ci",
    deadline=None,
    max_examples=10,
    suppress_health_check=[HealthCheck.too_slow]
)

settings.load_profile("ci")

logger = logging.getLogger(__name__)


@pytest.fixture()
def payments_health_services():
    client_service = TestClient(app)
    logger.info("Instanciando PaymentsAPI para tests de healthcheck")
    return PaymentsAPI(client_service)  # Instancia de PaymentsAPI para usar en tests de healthcheck


@pytest.fixture()
def payments_transfer_services():
    client_service = TestClient(app)
    logger.info("Instanciando PaymentsAPI para tests de transferencias")
    return PaymentsAPI(client_service)  # Instancia de PaymentsAPI para usar en tests de transferencias


@pytest.fixture()
def storage_state():
    return {
        "transfers_db": transfers_db,
        "idempotency_index": idempotency_index,
    }


@pytest.fixture(autouse=True)
def clear_storage():
    """
    Fixture para limpiar el estado de la "base de datos" antes de cada test.
    """
    transfers_db.clear()
    idempotency_index.clear()
