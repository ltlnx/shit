import requests
from typing import Dict, List

class GitHubAPI:
    def __init__(self, token: str = None):
        self.base_url = "https://api.github.com"
        self.headers = {
            "Accept": "application/vnd.github.v3+json"
        }
        if token:
            self.headers["Authorization"] = f"token {token}"
            
    def get_trending_repos(self, language: str = None, since: str = "daily") -> List[Dict]:
        params = {
            "q": f"created:>{self._get_date_filter(since)}",
            "sort": "stars",
            "order": "desc"
        }
        if language:
            params["q"] += f" language:{language}"
            
        return self._make_request("/search/repositories", params)
        
    def _make_request(self, endpoint: str, params: Dict = None) -> Dict:
        response = requests.get(
            f"{self.base_url}{endpoint}",
            headers=self.headers,
            params=params
        )
        return response.json()