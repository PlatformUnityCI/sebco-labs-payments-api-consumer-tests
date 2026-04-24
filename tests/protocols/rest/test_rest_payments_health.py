import pytest


@pytest.mark.regression
@pytest.mark.payments
class TestPaymentsHealth:
    def test_healthcheck_returns_ok(self, payments_health_services):

        response = payments_health_services.get_health()
        body = response.json()

        assert response.status_code == 200
        assert body == {"status": "ok"}

        print("Health check response:", body)
