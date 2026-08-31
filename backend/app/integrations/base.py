import abc
from typing import Any, Dict, Optional

class BaseIntegrationAdapter(abc.ABC):
    def __init__(self, config: Dict[str, Any]):
        self.config = config

    @abc.abstractmethod
    async def test_connection(self) -> bool:
        pass

    @abc.abstractmethod
    async def sync_data(self, entity_type: str, data: Dict[str, Any]) -> Dict[str, Any]:
        pass

    @abc.abstractmethod
    def verify_webhook_signature(self, payload: bytes, signature: str) -> bool:
        pass
