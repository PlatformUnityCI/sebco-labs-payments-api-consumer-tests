from fastapi.testclient import TestClient
from commons_qa import logger

class ApiClient:
    """
    Client HTTP síncrono para test usando TestClient de FastAPI.
    """
    def __init__(self, client: TestClient):
        self.client = client
        self._logging = logger.get_logger(self.__class__.__name__)

    def get(self, path:str, params: dict | None = None, headers: dict | None = None):
        self._logging.info(f"GET {path}")

        response = self.client.get(
            path,
            params=params,
            headers=headers
            
        )
        return response

    def post(self, 
             path:str, 
             json: dict | None = None, 
             params: dict | None = None, 
             headers: dict | None = None
):
            self._logging.info(f"POST {path}")
            return self.client.post(
                path,
                json=json,
                params=params,
                headers=headers
            )