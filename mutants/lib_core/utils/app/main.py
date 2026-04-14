
from fastapi import FastAPI, HTTPException, status

from lib_core.utils.app.schemas import (
    CreateTransferRequest,
    ErrorResponse,
    TransferResponse,
)
from lib_core.utils.app.services import create_transfer, get_transfer

app = FastAPI(title="FastAPI QA Payments Lab", version="1.0.0")
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


@app.get("/health")
def healthcheck() -> dict:
    return {"status": "ok"}


@app.post(
    "/transfers",
    response_model=TransferResponse,
    status_code=status.HTTP_202_ACCEPTED,
    responses={
        400: {"model": ErrorResponse},
        409: {"model": ErrorResponse},
    },
)
def create_transfer_endpoint(payload: CreateTransferRequest):
    if payload.currency.upper() != "ARS":
        raise HTTPException(
            status_code=400,
            detail={
                "error_code": "UNSUPPORTED_CURRENCY",
                "message": "Only ARS is supported",
            },
        )

    transfer, _ = create_transfer(payload.model_dump())
    return transfer


@app.get(
    "/transfers/{transfer_id}",
    response_model=TransferResponse,
    responses={404: {"model": ErrorResponse}},
)
def get_transfer_endpoint(transfer_id: str):
    transfer = get_transfer(transfer_id)

    if not transfer:
        raise HTTPException(
            status_code=404,
            detail={
                "error_code": "TRANSFER_NOT_FOUND",
                "message": "Transfer was not found",
            },
        )

    return transfer
