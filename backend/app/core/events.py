from typing import Any, Callable, Dict, List
import asyncio
from backend.app.core.logging import logger

class DomainEvent:
    def __init__(self, name: str, tenant_id: str, payload: Dict[str, Any], actor_id: str = None):
        self.name = name
        self.tenant_id = tenant_id
        self.payload = payload
        self.actor_id = actor_id
        self.timestamp = asyncio.get_event_loop().time()

class EventBus:
    def __init__(self):
        self._handlers: Dict[str, List[Callable]] = {}

    def subscribe(self, event_name: str, handler: Callable):
        if event_name not in self._handlers:
            self._handlers[event_name] = []
        self._handlers[event_name].append(handler)
        logger.info(f"Registered event listener for domain event: '{event_name}'")

    async def publish(self, event: DomainEvent):
        logger.info(f"Publishing domain event: {event.name} (Tenant: {event.tenant_id})")
        handlers = self._handlers.get(event.name, [])
        for handler in handlers:
            try:
                if asyncio.iscoroutinefunction(handler):
                    asyncio.create_task(handler(event))
                else:
                    handler(event)
            except Exception as e:
                logger.error(f"Error executing handler for event {event.name}: {str(e)}", exc_info=True)

event_bus = EventBus()
