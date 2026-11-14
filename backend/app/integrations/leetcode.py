import httpx
import json
from typing import Dict, Any
from app.integrations.base import PlatformIntegration

LEETCODE_GRAPHQL_URL = "https://leetcode.com/graphql"
HEADERS = {
    "Content-Type": "application/json",
    "Referer": "https://leetcode.com",
}

STATS_QUERY = """
query getUserProfile($username: String!) {
  matchedUser(username: $username) {
    username
    submitStats: submitStatsGlobal {
      acSubmissionNum {
        difficulty
        count
        submissions
      }
    }
    profile {
      ranking
      reputation
      starRating
    }
  }
}
"""

CALENDAR_QUERY = """
query userProfileCalendar($username: String!, $year: Int) {
  matchedUser(username: $username) {
    userCalendar(year: $year) {
      activeYears
      streak
      totalActiveDays
      submissionCalendar
    }
  }
}
"""

CONTEST_QUERY = """
query userContestRankingInfo($username: String!) {
  userContestRanking(username: $username) {
    attendedContestsCount
    rating
    globalRanking
    totalParticipants
    topPercentage
  }
  userContestRankingHistory(username: $username) {
    attended
    rating
    ranking
    contest {
      title
      startTime
    }
  }
}
"""


class LeetCodeIntegration(PlatformIntegration):
    def platform_name(self) -> str:
        return "leetcode"

    async def fetch_stats(self, username: str) -> Dict[str, Any]:
        async with httpx.AsyncClient(timeout=30.0) as client:
            # Fetch user stats
            stats_resp = await client.post(
                LEETCODE_GRAPHQL_URL,
                headers=HEADERS,
                json={"query": STATS_QUERY, "variables": {"username": username}},
            )
            stats_data = stats_resp.json()

            matched_user = stats_data.get("data", {}).get("matchedUser")
            if not matched_user:
                return {
                    "available": False,
                    "error": "User not found on LeetCode",
                    "username": username,
                }

            # Parse submission stats
            submission_stats = matched_user.get("submitStats", {}).get("acSubmissionNum", [])
            total_solved = 0
            easy_solved = 0
            medium_solved = 0
            hard_solved = 0
            easy_submissions = 0
            medium_submissions = 0
            hard_submissions = 0

            for entry in submission_stats:
                diff = entry.get("difficulty", "").lower()
                count = entry.get("count", 0)
                subs = entry.get("submissions", 0)
                if diff == "all":
                    total_solved = count
                elif diff == "easy":
                    easy_solved = count
                    easy_submissions = subs
                elif diff == "medium":
                    medium_solved = count
                    medium_submissions = subs
                elif diff == "hard":
                    hard_solved = count
                    hard_submissions = subs

            profile_info = matched_user.get("profile", {})
            ranking = profile_info.get("ranking", 0)

            # Fetch calendar
            streak = 0
            total_active_days = 0
            submission_calendar: Dict = {}
            try:
                cal_resp = await client.post(
                    LEETCODE_GRAPHQL_URL,
                    headers=HEADERS,
                    json={"query": CALENDAR_QUERY, "variables": {"username": username}},
                )
                cal_data = cal_resp.json()
                cal_user = cal_data.get("data", {}).get("matchedUser", {})
                user_calendar = cal_user.get("userCalendar", {}) if cal_user else {}
                streak = user_calendar.get("streak", 0)
                total_active_days = user_calendar.get("totalActiveDays", 0)
                raw_calendar = user_calendar.get("submissionCalendar", "{}")
                submission_calendar = json.loads(raw_calendar) if isinstance(raw_calendar, str) else {}
            except Exception:
                pass

            # Fetch contest info
            contest_rating = 0.0
            contests_attended = 0
            contest_history = []
            try:
                contest_resp = await client.post(
                    LEETCODE_GRAPHQL_URL,
                    headers=HEADERS,
                    json={"query": CONTEST_QUERY, "variables": {"username": username}},
                )
                contest_data = contest_resp.json()
                contest_ranking = contest_data.get("data", {}).get("userContestRanking") or {}
                contest_rating = contest_ranking.get("rating", 0.0) or 0.0
                contests_attended = contest_ranking.get("attendedContestsCount", 0) or 0
                history_raw = contest_data.get("data", {}).get("userContestRankingHistory") or []
                for h in history_raw:
                    if h.get("attended"):
                        contest_history.append({
                            "title": h.get("contest", {}).get("title", ""),
                            "start_time": h.get("contest", {}).get("startTime"),
                            "rating": h.get("rating"),
                            "ranking": h.get("ranking"),
                        })
            except Exception:
                pass

            return {
                "username": username,
                "total_solved": total_solved,
                "easy_solved": easy_solved,
                "medium_solved": medium_solved,
                "hard_solved": hard_solved,
                "easy_submissions": easy_submissions,
                "medium_submissions": medium_submissions,
                "hard_submissions": hard_submissions,
                "ranking": ranking,
                "streak": streak,
                "total_active_days": total_active_days,
                "submission_calendar": submission_calendar,
                "contest_rating": float(contest_rating),
                "contests_attended": contests_attended,
                "contest_history": contest_history,
                "available": True,
                "error": None,
            }
