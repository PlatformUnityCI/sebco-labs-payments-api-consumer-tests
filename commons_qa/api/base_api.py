class BaseApi:
    def __init__(self, client:APIClient)
        self.client = client

    def _headers(self, extra:dict | None = None):
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
        }
        if extra:
            headers.update(extra)
        return headers