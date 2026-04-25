from fastapi.testclient import TestClient
from lib_core.utils.app.main import app
from lib_core.utils.apis.rest.payments_api import PaymentsAPI
from lib_core.utils.app.storage import transfers_db, idempotency_index


def before_scenario(context, scenario):
    # equivalente a tus fixtures
    client = TestClient(app)

    context.payments_api = PaymentsAPI(client)

    context.storage_state = {
        "transfers_db": transfers_db,
        "idempotency_index": idempotency_index,
    }

    # 🔥 equivalente a autouse fixture
    transfers_db.clear()
    idempotency_index.clear()
