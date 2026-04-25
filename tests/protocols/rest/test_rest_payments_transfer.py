import pytest
import json


@pytest.mark.regression
@pytest.mark.payments_rest
class TestPaymentsTransfer:

    # 🔹 "Background" → contexto común
    def _given_valid_transfer(self):
        return {
            "from_account_id": "ACC-001",
            "to_alias": "alias.destino",
            "amount": 250,
            "currency": "ARS",
            "idempotency_key": "IDEMP-001",
        }

    def _given_empty_storage(self, storage_state):
        storage_state["transfers_db"].clear()

    # 🔹 "When"
    def _when_create_transfer(self, payments_transfer_services, payload=None):
        return payments_transfer_services.post_transfer(payload)

    # 🔹 "Then" (assertions reutilizables)
    def _then_status_is(self, response, expected_status):
        assert response.status_code == expected_status

    def _then_transfer_is_pending(self, body):
        assert body["state"] == "PENDING"

    def _then_transfer_data_is_correct(self, body, payload):
        expected_amount = payload["amount"]

        if isinstance(expected_amount, (str, bool)):
            expected_amount = float(expected_amount)

        assert body["amount"] == expected_amount
        assert body["currency"] == payload["currency"]
        assert body["idempotency_key"] == payload["idempotency_key"]

    def _then_transfer_id_is_valid(self, body):
        assert body["transfer_id"] is not None
        assert body["transfer_id"].startswith("TRF-")

    def _then_transfer_is_stored(self, body, storage_state):
        transfer_id = body["transfer_id"]
        assert transfer_id in storage_state["transfers_db"]
        assert storage_state["transfers_db"][transfer_id] is not None

    # 🔹 Escenario base (tu test original mejor estructurado)
    def test_create_transfer(self, payments_transfer_services, storage_state):

        # Given
        payload = self._given_valid_transfer()
        self._given_empty_storage(storage_state)

        # When
        response = self._when_create_transfer(
            payments_transfer_services,
            payload=payload)
        body = response.json()

        # Then
        self._then_status_is(response, 202)
        self._then_transfer_is_pending(body)
        self._then_transfer_data_is_correct(body, payload)
        self._then_transfer_id_is_valid(body)
        self._then_transfer_is_stored(body, storage_state)

    # 🔹 "Scenario Outline" → múltiples casos
    @pytest.mark.parametrize("amount, expected_status, expected_error_type",
                             [
                                 (250.0, 202, None),                             # valor típico válido (caso normal)
                                 (0.01, 202, None),                              # límite inferior válido (apenas mayor a 0)

                                 # límites y casos inválidos para validar la robustez de la API frente a inputs no esperados o maliciosos
                                 (0, 422, "greater_than"),                       # límite inferior inválido (igual a 0)
                                 # valor negativo inválido (fuera del dominio)
                                 (-10, 422, "greater_than"),
                                 (-0.01, 422, "greater_than"),                   # apenas por debajo del límite inferior
                                 # valor alto válido (prueba de límite superior / stress)
                                 (1_000_000, 202, None),
                                 # (100000000_000_000.01, 422),                  # apenas por encima del límite superior (si existe validación)

                                 # tipos y formatos inválidos para probar la validación de tipos y formatos en la API
                                 ("abc", 422, "float_parsing"),                  # string inválido
                                 (None, 422, "float_type"),                      # null
                                 ([100], 422, "float_type"),                     # tipo incorrecto

                                 # validación de tipo y lo convierte a número, podría ser interpretado como 1 (si toma el primer elemento del array) o lanzar un error de validación
                                 # coerción de string numérico, podría ser interpretado como 100 o lanzar un error de validación
                                 ("100", 202, None),
                                 # coerción a 1, podría ser interpretado como 1 o lanzar un error de validación
                                 (True, 202, None),
                             ]
                             )
    def test_create_transfer_with_different_amounts(
        self,
        payments_transfer_services,
        storage_state,
        amount,
        expected_status,
        expected_error_type
    ):
        # Given
        payload = self._given_valid_transfer()
        payload["amount"] = amount
        self._given_empty_storage(storage_state)

        # When
        print(f"\nRequest payload: {json.dumps(payload, indent=2, default=str)}")

        response = self._when_create_transfer(
            payments_transfer_services,
            payload=payload)
        body = response.json()

        respuesta_formateada = json.dumps(body, indent=2, ensure_ascii=False)
        print("Create transfer response:", respuesta_formateada)

        # Then
        self._then_status_is(response, expected_status)

        if expected_status == 202:
            self._then_transfer_is_pending(body)
            self._then_transfer_data_is_correct(body, payload)
        elif expected_status == 422:
            assert "detail" in body
            assert any(
                error["type"] == expected_error_type
                for error in body["detail"]
            )
