
from uuid import uuid4

from lib_core.utils.app.storage import transfers_db, idempotency_index


def create_transfer(data: dict) -> tuple[dict, bool]:
    """
    Returns:
      (transfer, created_new)
    """
    idem_key = data["idempotency_key"]

    if idem_key in idempotency_index:
        transfer_id = idempotency_index[idem_key]
        return transfers_db[transfer_id], False

    transfer_id = f"TRF-{uuid4().hex[:8].upper()}"
    transfer = {
        "transfer_id": transfer_id,
        "state": "PENDING",
        "amount": data["amount"],
        "currency": data["currency"],
        "from_account_id": data["from_account_id"],
        "to_alias": data["to_alias"],
        "idempotency_key": idem_key,
    }

    transfers_db[transfer_id] = transfer
    idempotency_index[idem_key] = transfer_id
    return transfer, True


def get_transfer(transfer_id: str) -> dict | None:
    return transfers_db.get(transfer_id)
