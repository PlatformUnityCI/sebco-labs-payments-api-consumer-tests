import pytest

@pytest.mark.regression
@pytest.mark.payments
class TestPaymentsTransfer:
    def test_create_transfer(self, payments_transfer_services, storage_state):

        response = payments_transfer_services.post_transfer()
        body = response.json()

        assert response.status_code == 202
        assert body["state"] == "PENDING"

        assert body["amount"] == 250.0
        assert body["currency"] == "ARS"
        assert body["idempotency_key"] == "IDEMP-001"
        assert body["transfer_id"] is not None
        assert body["transfer_id"].startswith("TRF-")

        assert body["transfer_id"] in storage_state["transfers_db"]
        assert storage_state["transfers_db"][body["transfer_id"]] is not None

        print("Create transfer response:", body)