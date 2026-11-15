from abc import ABC, abstractmethod
from typing import Dict, Any


class PlatformIntegration(ABC):
    @abstractmethod
    async def fetch_stats(self, username: str) -> Dict[str, Any]:
        pass

    @abstractmethod
    def platform_name(self) -> str:
        pass
