import httpx
from typing import Dict, Any
from app.integrations.base import PlatformIntegration

HACKERRANK_BASE = "https://www.hackerrank.com/rest/hackers"


class HackerRankIntegration(PlatformIntegration):
    def platform_name(self) -> str:
        return "hackerrank"

    async def fetch_stats(self, username: str) -> Dict[str, Any]:
        try:
            async with httpx.AsyncClient(timeout=15.0) as client:
                resp = await client.get(
                    f"{HACKERRANK_BASE}/{username}/scores_elo",
                    headers={"User-Agent": "Mozilla/5.0"},
                )
                if resp.status_code == 200:
                    data = resp.json()
                    return {
                        "available": True,
                        "username": username,
                        "scores": data,
                        "error": None,
                    }
                else:
                    return {
                        "available": False,
                        "error": "HackerRank public API unavailable",
                        "username": username,
                    }
        except Exception:
            return {
                "available": False,
                "error": "HackerRank public API unavailable",
                "username": username,
            }
