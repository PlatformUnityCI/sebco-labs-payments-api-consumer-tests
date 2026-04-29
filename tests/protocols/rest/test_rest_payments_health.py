import pytest
import logging

@pytest.mark.regression
@pytest.mark.payments_behave
class TestPaymentsHealth:
    def test_healthcheck_returns_ok(self, payments_health_services):

        response = payments_health_services.get_health()
        body = response.json()

        assert response.status_code == 200
        assert body == {"status": "ok"}

        logging.info("Health check response: %s", body)
