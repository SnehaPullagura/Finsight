import abc
import enum
import datetime
from typing import Dict, List, Optional, Any
from pydantic import BaseModel, Field

class AAConsentStatus(str, enum.Enum):
    REQUESTED = "REQUESTED"
    APPROVED = "APPROVED"
    ACTIVE = "ACTIVE"
    PAUSED = "PAUSED"
    REVOKED = "REVOKED"
    EXPIRED = "EXPIRED"
    FAILED = "FAILED"

class AADataFrequency(str, enum.Enum):
    ONETIME = "ONETIME"
    DAILY = "DAILY"
    WEEKLY = "WEEKLY"
    MONTHLY = "MONTHLY"
    REALTIME = "REALTIME"

class AAConsentArtifact(BaseModel):
    consent_id: str
    consent_handle: str
    user_id: int
    user_vpa: str
    status: AAConsentStatus
    frequency: AADataFrequency
    fi_types: List[str] = ["DEPOSIT", "TERM_DEPOSIT", "RECURRING_DEPOSIT", "MUTUAL_FUNDS", "EQUITIES"]
    date_range_from: datetime.date
    date_range_to: datetime.date
    consent_start: datetime.datetime
    consent_expiry: datetime.datetime
    data_filter_type: str = "TRANSACTION"
    data_life_unit: str = "YEAR"
    data_life_value: int = 3
    signature: Optional[str] = None
    created_at: datetime.datetime = Field(default_factory=datetime.datetime.utcnow)

class AAEncryptedDataPayload(BaseModel):
    session_id: str
    account_aggregator_id: str
    key_material: Dict[str, str]
    encrypted_fi_data: str
    fip_id: str
    signature: str

class BaseAccountAggregatorAdapter(abc.ABC):
    @abc.abstractmethod
    async def create_consent_request(self, user_id: int, user_vpa: str, fi_types: List[str], date_range_days: int) -> AAConsentArtifact:
        pass

    @abc.abstractmethod
    async def check_consent_status(self, consent_handle: str) -> AAConsentStatus:
        pass

    @abc.abstractmethod
    async def fetch_financial_data(self, consent_id: str, private_key_pem: str) -> List[Dict[str, Any]]:
        pass

    @abc.abstractmethod
    async def revoke_consent(self, consent_id: str) -> bool:
        pass
