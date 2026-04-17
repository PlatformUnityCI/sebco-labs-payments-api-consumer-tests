
from enum import Enum
from pydantic import BaseModel, Field


class TransferState(str, Enum):
    PENDING = "PENDING"
    COMPLETED = "COMPLETED"
    CANCELLED = "CANCELLED"


class CreateTransferRequest(BaseModel):
    from_account_id: str = Field(..., min_length=1)
    to_alias: str = Field(..., min_length=3)
    amount: float = Field(..., gt=0)
    currency: str = Field(..., min_length=3, max_length=3)
    idempotency_key: str = Field(..., min_length=3)


class TransferResponse(BaseModel):
    transfer_id: str
    state: TransferState
    amount: float
    currency: str
    from_account_id: str
    to_alias: str
    idempotency_key: str


class ErrorResponse(BaseModel):
    error_code: str
    message: str
