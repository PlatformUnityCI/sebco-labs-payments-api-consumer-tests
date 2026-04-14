
from fastapi import FastAPI, HTTPException, status

from lib_core.utils.app.schemas import (
    CreateTransferRequest,
    ErrorResponse,
    TransferResponse,
)
from lib_core.utils.app.services import create_transfer, get_transfer

app = FastAPI(title="FastAPI QA Payments Lab", version="1.0.0")


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
