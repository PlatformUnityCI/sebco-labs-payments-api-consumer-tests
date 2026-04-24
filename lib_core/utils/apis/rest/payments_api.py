from commons_qa.api.api_client import ApiClient


class PaymentsAPI(ApiClient):
    """
    Clase encargada de encapsular los endpoints de la API de Payments (health + transfer).
    """

    def __init__(self, client):
        super().__init__(client)  # El ApiClient se inyectará en los tests a través de la fixture

    def get_health(self):
        return self.get("/health")

    def post_transfer(self, payload=None):
        return self.post("/transfers", json=payload)

    def get_transfer(self, transfer_id: str):
        return self.get(f"/transfers/{transfer_id}")
