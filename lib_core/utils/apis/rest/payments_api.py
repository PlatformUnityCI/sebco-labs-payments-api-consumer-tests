from commons_qa.api.api_client import ApiClient

def build_transfer_payload():
    return {
        "from_account_id": "ACC-001",
        "to_alias": "alias.destino",
        "amount": 250.0,
        "currency": "ARS",
        "idempotency_key": "IDEMP-001",
    }

class PaymentsAPI(ApiClient):
    """
    Clase encargada de encapsular los endpoints de la API de Payments (health + transfer).
    """

    def __init__(self, client):
        super().__init__(client)  # El ApiClient se inyectará en los tests a través de la fixture

    def get_health(self):
        return self.get("/health")

    def post_transfer(self, payload=None):
        if payload is None:
            payload = build_transfer_payload()
        return self.post("/transfers", json=payload)

    def get_transfer(self, transfer_id: str):
        return self.get(f"/transfers/{transfer_id}")