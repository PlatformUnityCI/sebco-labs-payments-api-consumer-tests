from behave import *
import json
import logging


@given("el storage de transferencias está vacío")
def step_clear_storage(context):
    context.storage_state["transfers_db"].clear()


@given("existe un payload base de transferencia válido")
def step_valid_payload(context):
    context.payload = {
        "from_account_id": "ACC-001",
        "to_alias": "alias.destino",
        "amount": 250,
        "currency": "ARS",
        "idempotency_key": "IDEMP-001",
    }


@given('modifico el amount a "{amount}"')
def step_modify_amount(context, amount):

    if amount == "null":
        parsed = None
    elif amount == "true":
        parsed = True
    elif amount.startswith("["):
        parsed = [100]
    else:
        try:
            parsed = float(amount)
        except Exception:
            parsed = amount

    context.payload["amount"] = parsed


@when("envío la transferencia")
def step_send_transfer(context):
    response = context.payments_api.post_transfer(context.payload)
    context.response = response
    context.body = response.json()

    logging.info("\nRequest: %s", json.dumps(context.payload, indent=2, default=str))
    logging.info("Response: %s", json.dumps(context.body, indent=2, ensure_ascii=False))


@then("el status code es {status:d}")
def step_status_code(context, status):
    assert context.response.status_code == status


@then('el estado de la transferencia es "{state}"')
def step_state(context, state):
    assert context.body["state"] == state


@then("los datos de la transferencia son correctos")
def step_validate_data(context):
    payload = context.payload

    expected_amount = payload["amount"]
    if isinstance(expected_amount, (str, bool)):
        expected_amount = float(expected_amount)

    assert context.body["amount"] == expected_amount
    assert context.body["currency"] == payload["currency"]
    assert context.body["idempotency_key"] == payload["idempotency_key"]


@then("el transfer_id es válido")
def step_transfer_id(context):
    assert context.body["transfer_id"].startswith("TRF-")


@then("la transferencia se guarda en storage")
def step_storage(context):
    transfer_id = context.body["transfer_id"]
    assert transfer_id in context.storage_state["transfers_db"]


@then('el error es de tipo "{error_type}"')
def step_error_type(context, error_type):
    assert "detail" in context.body

    assert any(
        error["type"] == error_type
        for error in context.body["detail"]
    )


@then('el error contiene el tipo "{error_type}"')
def step_impl(context, error_type):
    response = context.response.json()

    if error_type == "none":
        # Caso éxito: no debería haber error
        assert "detail" not in response, f"Se esperaba sin error y vino: {response}"
    else:
        assert "detail" in response, "Se esperaba error pero no vino"
        actual_error = response["detail"][0]["type"]
        assert actual_error == error_type, f"Esperado: {error_type}, Actual: {actual_error}"
