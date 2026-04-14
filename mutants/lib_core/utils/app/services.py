
from uuid import uuid4

from lib_core.utils.app.storage import transfers_db, idempotency_index
from typing import Annotated
from typing import Callable
from typing import ClassVar

MutantDict = Annotated[dict[str, Callable], "Mutant"] # type: ignore


def _mutmut_trampoline(orig, mutants, call_args, call_kwargs, self_arg = None): # type: ignore
    """Forward call to original or mutated function, depending on the environment"""
    import os # type: ignore
    mutant_under_test = os.environ['MUTANT_UNDER_TEST'] # type: ignore
    if mutant_under_test == 'fail': # type: ignore
        from mutmut.__main__ import MutmutProgrammaticFailException # type: ignore
        raise MutmutProgrammaticFailException('Failed programmatically')       # type: ignore
    elif mutant_under_test == 'stats': # type: ignore
        from mutmut.__main__ import record_trampoline_hit # type: ignore
        record_trampoline_hit(orig.__module__ + '.' + orig.__name__) # type: ignore
        # (for class methods, orig is bound and thus does not need the explicit self argument)
        result = orig(*call_args, **call_kwargs) # type: ignore
        return result # type: ignore
    prefix = orig.__module__ + '.' + orig.__name__ + '__mutmut_' # type: ignore
    if not mutant_under_test.startswith(prefix): # type: ignore
        result = orig(*call_args, **call_kwargs) # type: ignore
        return result # type: ignore
    mutant_name = mutant_under_test.rpartition('.')[-1] # type: ignore
    if self_arg is not None: # type: ignore
        # call to a class method where self is not bound
        result = mutants[mutant_name](self_arg, *call_args, **call_kwargs) # type: ignore
    else:
        result = mutants[mutant_name](*call_args, **call_kwargs) # type: ignore
    return result # type: ignore


def create_transfer(data: dict) -> tuple[dict, bool]:
    args = [data]# type: ignore
    kwargs = {}# type: ignore
    return _mutmut_trampoline(x_create_transfer__mutmut_orig, x_create_transfer__mutmut_mutants, args, kwargs, None)


def x_create_transfer__mutmut_orig(data: dict) -> tuple[dict, bool]:
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


def x_create_transfer__mutmut_1(data: dict) -> tuple[dict, bool]:
    """
    Returns:
      (transfer, created_new)
    """
    idem_key = None

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


def x_create_transfer__mutmut_2(data: dict) -> tuple[dict, bool]:
    """
    Returns:
      (transfer, created_new)
    """
    idem_key = data["XXidempotency_keyXX"]

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


def x_create_transfer__mutmut_3(data: dict) -> tuple[dict, bool]:
    """
    Returns:
      (transfer, created_new)
    """
    idem_key = data["IDEMPOTENCY_KEY"]

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


def x_create_transfer__mutmut_4(data: dict) -> tuple[dict, bool]:
    """
    Returns:
      (transfer, created_new)
    """
    idem_key = data["idempotency_key"]

    if idem_key not in idempotency_index:
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


def x_create_transfer__mutmut_5(data: dict) -> tuple[dict, bool]:
    """
    Returns:
      (transfer, created_new)
    """
    idem_key = data["idempotency_key"]

    if idem_key in idempotency_index:
        transfer_id = None
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


def x_create_transfer__mutmut_6(data: dict) -> tuple[dict, bool]:
    """
    Returns:
      (transfer, created_new)
    """
    idem_key = data["idempotency_key"]

    if idem_key in idempotency_index:
        transfer_id = idempotency_index[idem_key]
        return transfers_db[transfer_id], True

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


def x_create_transfer__mutmut_7(data: dict) -> tuple[dict, bool]:
    """
    Returns:
      (transfer, created_new)
    """
    idem_key = data["idempotency_key"]

    if idem_key in idempotency_index:
        transfer_id = idempotency_index[idem_key]
        return transfers_db[transfer_id], False

    transfer_id = None
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


def x_create_transfer__mutmut_8(data: dict) -> tuple[dict, bool]:
    """
    Returns:
      (transfer, created_new)
    """
    idem_key = data["idempotency_key"]

    if idem_key in idempotency_index:
        transfer_id = idempotency_index[idem_key]
        return transfers_db[transfer_id], False

    transfer_id = f"TRF-{uuid4().hex[:8].lower()}"
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


def x_create_transfer__mutmut_9(data: dict) -> tuple[dict, bool]:
    """
    Returns:
      (transfer, created_new)
    """
    idem_key = data["idempotency_key"]

    if idem_key in idempotency_index:
        transfer_id = idempotency_index[idem_key]
        return transfers_db[transfer_id], False

    transfer_id = f"TRF-{uuid4().hex[:9].upper()}"
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


def x_create_transfer__mutmut_10(data: dict) -> tuple[dict, bool]:
    """
    Returns:
      (transfer, created_new)
    """
    idem_key = data["idempotency_key"]

    if idem_key in idempotency_index:
        transfer_id = idempotency_index[idem_key]
        return transfers_db[transfer_id], False

    transfer_id = f"TRF-{uuid4().hex[:8].upper()}"
    transfer = None

    transfers_db[transfer_id] = transfer
    idempotency_index[idem_key] = transfer_id
    return transfer, True


def x_create_transfer__mutmut_11(data: dict) -> tuple[dict, bool]:
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
        "XXtransfer_idXX": transfer_id,
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


def x_create_transfer__mutmut_12(data: dict) -> tuple[dict, bool]:
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
        "TRANSFER_ID": transfer_id,
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


def x_create_transfer__mutmut_13(data: dict) -> tuple[dict, bool]:
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
        "XXstateXX": "PENDING",
        "amount": data["amount"],
        "currency": data["currency"],
        "from_account_id": data["from_account_id"],
        "to_alias": data["to_alias"],
        "idempotency_key": idem_key,
    }

    transfers_db[transfer_id] = transfer
    idempotency_index[idem_key] = transfer_id
    return transfer, True


def x_create_transfer__mutmut_14(data: dict) -> tuple[dict, bool]:
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
        "STATE": "PENDING",
        "amount": data["amount"],
        "currency": data["currency"],
        "from_account_id": data["from_account_id"],
        "to_alias": data["to_alias"],
        "idempotency_key": idem_key,
    }

    transfers_db[transfer_id] = transfer
    idempotency_index[idem_key] = transfer_id
    return transfer, True


def x_create_transfer__mutmut_15(data: dict) -> tuple[dict, bool]:
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
        "state": "XXPENDINGXX",
        "amount": data["amount"],
        "currency": data["currency"],
        "from_account_id": data["from_account_id"],
        "to_alias": data["to_alias"],
        "idempotency_key": idem_key,
    }

    transfers_db[transfer_id] = transfer
    idempotency_index[idem_key] = transfer_id
    return transfer, True


def x_create_transfer__mutmut_16(data: dict) -> tuple[dict, bool]:
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
        "state": "pending",
        "amount": data["amount"],
        "currency": data["currency"],
        "from_account_id": data["from_account_id"],
        "to_alias": data["to_alias"],
        "idempotency_key": idem_key,
    }

    transfers_db[transfer_id] = transfer
    idempotency_index[idem_key] = transfer_id
    return transfer, True


def x_create_transfer__mutmut_17(data: dict) -> tuple[dict, bool]:
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
        "XXamountXX": data["amount"],
        "currency": data["currency"],
        "from_account_id": data["from_account_id"],
        "to_alias": data["to_alias"],
        "idempotency_key": idem_key,
    }

    transfers_db[transfer_id] = transfer
    idempotency_index[idem_key] = transfer_id
    return transfer, True


def x_create_transfer__mutmut_18(data: dict) -> tuple[dict, bool]:
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
        "AMOUNT": data["amount"],
        "currency": data["currency"],
        "from_account_id": data["from_account_id"],
        "to_alias": data["to_alias"],
        "idempotency_key": idem_key,
    }

    transfers_db[transfer_id] = transfer
    idempotency_index[idem_key] = transfer_id
    return transfer, True


def x_create_transfer__mutmut_19(data: dict) -> tuple[dict, bool]:
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
        "amount": data["XXamountXX"],
        "currency": data["currency"],
        "from_account_id": data["from_account_id"],
        "to_alias": data["to_alias"],
        "idempotency_key": idem_key,
    }

    transfers_db[transfer_id] = transfer
    idempotency_index[idem_key] = transfer_id
    return transfer, True


def x_create_transfer__mutmut_20(data: dict) -> tuple[dict, bool]:
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
        "amount": data["AMOUNT"],
        "currency": data["currency"],
        "from_account_id": data["from_account_id"],
        "to_alias": data["to_alias"],
        "idempotency_key": idem_key,
    }

    transfers_db[transfer_id] = transfer
    idempotency_index[idem_key] = transfer_id
    return transfer, True


def x_create_transfer__mutmut_21(data: dict) -> tuple[dict, bool]:
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
        "XXcurrencyXX": data["currency"],
        "from_account_id": data["from_account_id"],
        "to_alias": data["to_alias"],
        "idempotency_key": idem_key,
    }

    transfers_db[transfer_id] = transfer
    idempotency_index[idem_key] = transfer_id
    return transfer, True


def x_create_transfer__mutmut_22(data: dict) -> tuple[dict, bool]:
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
        "CURRENCY": data["currency"],
        "from_account_id": data["from_account_id"],
        "to_alias": data["to_alias"],
        "idempotency_key": idem_key,
    }

    transfers_db[transfer_id] = transfer
    idempotency_index[idem_key] = transfer_id
    return transfer, True


def x_create_transfer__mutmut_23(data: dict) -> tuple[dict, bool]:
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
        "currency": data["XXcurrencyXX"],
        "from_account_id": data["from_account_id"],
        "to_alias": data["to_alias"],
        "idempotency_key": idem_key,
    }

    transfers_db[transfer_id] = transfer
    idempotency_index[idem_key] = transfer_id
    return transfer, True


def x_create_transfer__mutmut_24(data: dict) -> tuple[dict, bool]:
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
        "currency": data["CURRENCY"],
        "from_account_id": data["from_account_id"],
        "to_alias": data["to_alias"],
        "idempotency_key": idem_key,
    }

    transfers_db[transfer_id] = transfer
    idempotency_index[idem_key] = transfer_id
    return transfer, True


def x_create_transfer__mutmut_25(data: dict) -> tuple[dict, bool]:
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
        "XXfrom_account_idXX": data["from_account_id"],
        "to_alias": data["to_alias"],
        "idempotency_key": idem_key,
    }

    transfers_db[transfer_id] = transfer
    idempotency_index[idem_key] = transfer_id
    return transfer, True


def x_create_transfer__mutmut_26(data: dict) -> tuple[dict, bool]:
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
        "FROM_ACCOUNT_ID": data["from_account_id"],
        "to_alias": data["to_alias"],
        "idempotency_key": idem_key,
    }

    transfers_db[transfer_id] = transfer
    idempotency_index[idem_key] = transfer_id
    return transfer, True


def x_create_transfer__mutmut_27(data: dict) -> tuple[dict, bool]:
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
        "from_account_id": data["XXfrom_account_idXX"],
        "to_alias": data["to_alias"],
        "idempotency_key": idem_key,
    }

    transfers_db[transfer_id] = transfer
    idempotency_index[idem_key] = transfer_id
    return transfer, True


def x_create_transfer__mutmut_28(data: dict) -> tuple[dict, bool]:
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
        "from_account_id": data["FROM_ACCOUNT_ID"],
        "to_alias": data["to_alias"],
        "idempotency_key": idem_key,
    }

    transfers_db[transfer_id] = transfer
    idempotency_index[idem_key] = transfer_id
    return transfer, True


def x_create_transfer__mutmut_29(data: dict) -> tuple[dict, bool]:
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
        "XXto_aliasXX": data["to_alias"],
        "idempotency_key": idem_key,
    }

    transfers_db[transfer_id] = transfer
    idempotency_index[idem_key] = transfer_id
    return transfer, True


def x_create_transfer__mutmut_30(data: dict) -> tuple[dict, bool]:
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
        "TO_ALIAS": data["to_alias"],
        "idempotency_key": idem_key,
    }

    transfers_db[transfer_id] = transfer
    idempotency_index[idem_key] = transfer_id
    return transfer, True


def x_create_transfer__mutmut_31(data: dict) -> tuple[dict, bool]:
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
        "to_alias": data["XXto_aliasXX"],
        "idempotency_key": idem_key,
    }

    transfers_db[transfer_id] = transfer
    idempotency_index[idem_key] = transfer_id
    return transfer, True


def x_create_transfer__mutmut_32(data: dict) -> tuple[dict, bool]:
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
        "to_alias": data["TO_ALIAS"],
        "idempotency_key": idem_key,
    }

    transfers_db[transfer_id] = transfer
    idempotency_index[idem_key] = transfer_id
    return transfer, True


def x_create_transfer__mutmut_33(data: dict) -> tuple[dict, bool]:
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
        "XXidempotency_keyXX": idem_key,
    }

    transfers_db[transfer_id] = transfer
    idempotency_index[idem_key] = transfer_id
    return transfer, True


def x_create_transfer__mutmut_34(data: dict) -> tuple[dict, bool]:
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
        "IDEMPOTENCY_KEY": idem_key,
    }

    transfers_db[transfer_id] = transfer
    idempotency_index[idem_key] = transfer_id
    return transfer, True


def x_create_transfer__mutmut_35(data: dict) -> tuple[dict, bool]:
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

    transfers_db[transfer_id] = None
    idempotency_index[idem_key] = transfer_id
    return transfer, True


def x_create_transfer__mutmut_36(data: dict) -> tuple[dict, bool]:
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
    idempotency_index[idem_key] = None
    return transfer, True


def x_create_transfer__mutmut_37(data: dict) -> tuple[dict, bool]:
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
    return transfer, False

x_create_transfer__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
'x_create_transfer__mutmut_1': x_create_transfer__mutmut_1, 
    'x_create_transfer__mutmut_2': x_create_transfer__mutmut_2, 
    'x_create_transfer__mutmut_3': x_create_transfer__mutmut_3, 
    'x_create_transfer__mutmut_4': x_create_transfer__mutmut_4, 
    'x_create_transfer__mutmut_5': x_create_transfer__mutmut_5, 
    'x_create_transfer__mutmut_6': x_create_transfer__mutmut_6, 
    'x_create_transfer__mutmut_7': x_create_transfer__mutmut_7, 
    'x_create_transfer__mutmut_8': x_create_transfer__mutmut_8, 
    'x_create_transfer__mutmut_9': x_create_transfer__mutmut_9, 
    'x_create_transfer__mutmut_10': x_create_transfer__mutmut_10, 
    'x_create_transfer__mutmut_11': x_create_transfer__mutmut_11, 
    'x_create_transfer__mutmut_12': x_create_transfer__mutmut_12, 
    'x_create_transfer__mutmut_13': x_create_transfer__mutmut_13, 
    'x_create_transfer__mutmut_14': x_create_transfer__mutmut_14, 
    'x_create_transfer__mutmut_15': x_create_transfer__mutmut_15, 
    'x_create_transfer__mutmut_16': x_create_transfer__mutmut_16, 
    'x_create_transfer__mutmut_17': x_create_transfer__mutmut_17, 
    'x_create_transfer__mutmut_18': x_create_transfer__mutmut_18, 
    'x_create_transfer__mutmut_19': x_create_transfer__mutmut_19, 
    'x_create_transfer__mutmut_20': x_create_transfer__mutmut_20, 
    'x_create_transfer__mutmut_21': x_create_transfer__mutmut_21, 
    'x_create_transfer__mutmut_22': x_create_transfer__mutmut_22, 
    'x_create_transfer__mutmut_23': x_create_transfer__mutmut_23, 
    'x_create_transfer__mutmut_24': x_create_transfer__mutmut_24, 
    'x_create_transfer__mutmut_25': x_create_transfer__mutmut_25, 
    'x_create_transfer__mutmut_26': x_create_transfer__mutmut_26, 
    'x_create_transfer__mutmut_27': x_create_transfer__mutmut_27, 
    'x_create_transfer__mutmut_28': x_create_transfer__mutmut_28, 
    'x_create_transfer__mutmut_29': x_create_transfer__mutmut_29, 
    'x_create_transfer__mutmut_30': x_create_transfer__mutmut_30, 
    'x_create_transfer__mutmut_31': x_create_transfer__mutmut_31, 
    'x_create_transfer__mutmut_32': x_create_transfer__mutmut_32, 
    'x_create_transfer__mutmut_33': x_create_transfer__mutmut_33, 
    'x_create_transfer__mutmut_34': x_create_transfer__mutmut_34, 
    'x_create_transfer__mutmut_35': x_create_transfer__mutmut_35, 
    'x_create_transfer__mutmut_36': x_create_transfer__mutmut_36, 
    'x_create_transfer__mutmut_37': x_create_transfer__mutmut_37
}
x_create_transfer__mutmut_orig.__name__ = 'x_create_transfer'


def get_transfer(transfer_id: str) -> dict | None:
    args = [transfer_id]# type: ignore
    kwargs = {}# type: ignore
    return _mutmut_trampoline(x_get_transfer__mutmut_orig, x_get_transfer__mutmut_mutants, args, kwargs, None)


def x_get_transfer__mutmut_orig(transfer_id: str) -> dict | None:
    return transfers_db.get(transfer_id)


def x_get_transfer__mutmut_1(transfer_id: str) -> dict | None:
    return transfers_db.get(None)

x_get_transfer__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
'x_get_transfer__mutmut_1': x_get_transfer__mutmut_1
}
x_get_transfer__mutmut_orig.__name__ = 'x_get_transfer'
