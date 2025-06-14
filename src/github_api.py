import requests
from typing import Dict, List
from datetime import datetime, timedelta

class GitHubAPI:
    def __init__(self, token: str = None):
        self.base_url = "https://api.github.com"
        self.headers = {
            "Accept": "application/vnd.github.v3+json"
        }
        if token:
            self.headers["Authorization"] = f"token {token}"
    
    def _get_date_filter(self, since: str) -> str:
        today = datetime.now()
        if since == "daily":
            return (today - timedelta(days=1)).strftime("%Y-%m-%d")
        elif since == "weekly":
            return (today - timedelta(weeks=1)).strftime("%Y-%m-%d")
        elif since == "monthly":
            return (today - timedelta(days=30)).strftime("%Y-%m-%d")
        return today.strftime("%Y-%m-%d")

    def get_trending_repos(self, language: str = None, since: str = "daily") -> List[Dict]:
        params = {
            "q": f"created:>{self._get_date_filter(since)}",
            "sort": "stars",
            "order": "desc"
        }
        if language:
            params["q"] += f" language:{language}"
            
        return self._make_request("/search/repositories", params)
    
    def get_most_starred_repos(self, language: str = None, limit: int = 10) -> List[Dict]:
        params = {
            "q": "stars:>1000",
            "sort": "stars",
            "order": "desc",
            "per_page": limit
        }
        if language:
            params["q"] += f" language:{language}"
        
        return self._make_request("/search/repositories", params)
    
    def get_language_stats(self) -> Dict:
        """Get statistics about programming languages on GitHub"""
        params = {"q": "stars:>100", "per_page": 100}
        repos = self._make_request("/search/repositories", params)
        languages = {}
        
        for repo in repos.get("items", []):
            lang = repo.get("language")
            if lang:
                if lang not in languages:
                    languages[lang] = {"count": 0, "stars": 0}
                languages[lang]["count"] += 1
                languages[lang]["stars"] += repo.get("stargazers_count", 0)
        
        return languages
    
    def get_topic_stats(self, topics: List[str]) -> Dict:
        """Get statistics about specific topics on GitHub"""
        result = {}
        for topic in topics:
            params = {"q": f"topic:{topic}", "sort": "stars", "order": "desc"}
            data = self._make_request("/search/repositories", params)
            result[topic] = {
                "total_count": data.get("total_count", 0),
                "top_repos": data.get("items", [])[:5]
            }
        return result

    def _make_request(self, endpoint: str, params: Dict = None) -> Dict:
        response = requests.get(
            f"{self.base_url}{endpoint}",
            headers=self.headers,
            params=params
        )
        response.raise_for_status()
        return response.json()
