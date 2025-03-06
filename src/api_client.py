import requests
from requests.auth import HTTPBasicAuth

class APIClient:
    def __init__(self, base_url, username, password):
        self.base_url = base_url
        self.auth = HTTPBasicAuth(username, password)

    def fetch_data(self, endpoint):
        url = f"{self.base_url}{endpoint}"
        try:
            response = requests.get(url, auth=self.auth)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Erreur lors de la requête HTTP: {e}")
            return None

    def fetch_uri(self, uri):
        return self.fetch_data(uri)
