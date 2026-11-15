import httpx
from typing import Dict, Any
from app.integrations.base import PlatformIntegration

CODEFORCES_BASE = "https://codeforces.com/api"


class CodeforcesIntegration(PlatformIntegration):
    def platform_name(self) -> str:
        return "codeforces"

    async def fetch_stats(self, username: str) -> Dict[str, Any]:
        async with httpx.AsyncClient(timeout=30.0) as client:
            # Fetch user info
            try:
                info_resp = await client.get(
                    f"{CODEFORCES_BASE}/user.info",
                    params={"handles": username},
                )
                info_data = info_resp.json()
            except Exception as e:
                return {
                    "available": False,
                    "error": f"Failed to reach Codeforces API: {str(e)}",
                    "username": username,
                }

            if info_data.get("status") != "OK":
                return {
                    "available": False,
                    "error": info_data.get("comment", "Unknown error from Codeforces API"),
                    "username": username,
                }

            user_info = info_data["result"][0]
            handle = user_info.get("handle", username)
            rating = user_info.get("rating", 0)
            max_rating = user_info.get("maxRating", 0)
            rank = user_info.get("rank", "unrated")
            max_rank = user_info.get("maxRank", "unrated")
            contribution = user_info.get("contribution", 0)
            avatar = user_info.get("avatar", "")

            # Fetch rating history for contest count
            contests_participated = 0
            try:
                rating_resp = await client.get(
                    f"{CODEFORCES_BASE}/user.rating",
                    params={"handle": username},
                )
                rating_data = rating_resp.json()
                if rating_data.get("status") == "OK":
                    contests_participated = len(rating_data.get("result", []))
            except Exception:
                pass

            return {
                "handle": handle,
                "rating": rating,
                "max_rating": max_rating,
                "rank": rank,
                "max_rank": max_rank,
                "contests_participated": contests_participated,
                "contribution": contribution,
                "avatar": avatar,
                "available": True,
                "error": None,
            }
