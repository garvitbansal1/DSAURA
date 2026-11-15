from typing import Dict, Any
from app.integrations.base import PlatformIntegration


class GFGIntegration(PlatformIntegration):
    def platform_name(self) -> str:
        return "geeksforgeeks"

    async def fetch_stats(self, username: str) -> Dict[str, Any]:
        return {
            "available": False,
            "platform": "geeksforgeeks",
            "reason": "GeeksforGeeks does not provide a public API. Use CSV import feature.",
            "username": username,
        }
