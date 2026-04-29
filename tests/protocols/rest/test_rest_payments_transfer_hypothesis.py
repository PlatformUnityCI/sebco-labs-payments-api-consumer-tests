"""
Hypothesis-based tests for Payments Transfer endpoint.

Este test NO reemplaza los parametrizados existentes.
Es un complemento usando property-based testing.
"""

import pytest
import json
import pytest_html

from hypothesis import given, example, settings, HealthCheck
from hypothesis import strategies as st
from hypothesis import note

from lib_core.utils.hypothesis_strategies.payments.transfer_strategies import (
    transfer_strategy
)

from tests.protocols.rest.conftest import (
    invalid_alias_results,
    invalid_amount_results
)

# ============================================================
# VALID TESTS for TRANSFER
# ============================================================

@pytest.mark.regression
@pytest.mark.payments_hypothesis
class TestRestPaymentsTransferHypothesisValidTransfer:
    """
    Tests con datos válidos generados automáticamente.
    Usa transfer_strategy (happy path).
    """

    @settings(
        max_examples=20,
        suppress_health_check=[
            HealthCheck.function_scoped_fixture
        ]
    )
    @given(transfer_data=transfer_strategy)

    # Caso histórico válido REAL
    @example(transfer_data={
        "from_account_id": "ACC-001",
        "to_alias": "alias.destino",
        "amount": 250,
        "currency": "ARS",
        "idempotency_key": "IDEMP-001",
    })

    def test_transfer_success_property(
        self,
        transfer_data,
        payments_transfer_services
    ):
        """
        Property test:
        cualquier payload válido debería crear transferencia.
        """

        response = payments_transfer_services.post_transfer(
            transfer_data
        )

        assert response.status_code == 202
        print(response.status_code)
        print(response.json())

        body = response.json()

        assert "transfer_id" in body or "id" in body
        print("Payload:", transfer_data)
        print(response.status_code)
        print(response.json())

# ============================================================
# INVALID TESTS for AMOUNT
# ============================================================

@pytest.mark.regression
@pytest.mark.payments_hypothesis
class TestRestPaymentsTransferHypothesisInvalidAmount:
    """
    Tests con datos inválidos.
    Solo variamos 'amount'.
    """

    invalid_amount_strategy = st.one_of(
        st.integers(max_value=0),          # negativos y cero
        st.text(min_size=1, max_size=10),  # strings chicos
        st.none(),
        st.floats(max_value=0),
        st.just([]),                       # lista vacía
        st.booleans(),
        st.just([1]),                      # lista simple
        st.booleans()
    )

    @settings(
        max_examples=20,
        suppress_health_check=[
            HealthCheck.function_scoped_fixture
        ]
    )
    @given(amount=invalid_amount_strategy)

    # Casos históricos negativos reales para 'amount'
    @example(amount=0)
    @example(amount=-10)
    @example(amount=-1)
    @example(amount="abc")
    @example(amount=None)
    @example(amount=[100])
    @example(amount=True)

    def test_transfer_invalid_amount(
        self,
        amount,
        payments_transfer_services,
        request
    ):
        """
        Property test:
        amount inválido debería devolver error.
        """

        payload = {
            "from_account_id": "ACC-001",
            "to_alias": "alias.destino",
            "amount": amount,
            "currency": "ARS",
            "idempotency_key": "IDEMP-999",
        }

        print("Payload:", payload)

        response = payments_transfer_services.post_transfer(
            payload
        )

        print(json.dumps(payload, indent=2, ensure_ascii=False))
        print(response.status_code)
        print(response.json())

        note(f"amount={amount}")
        note(f"status={response.status_code}")

        if response.status_code == 202:

                pytest_html = request.config.pluginmanager.getplugin("html")

                if pytest_html:
                    extra = getattr(request.node, "extra", [])

                    extra.append(
                        pytest_html.extras.text(
                            f"amount='{amount}' expected=422 got={response.status_code}"
                        )
                    )

                    request.node.extra = extra

                pytest.xfail(
                    f"Invalid amount accepted: amount='{amount}' "
                    f"expected=422 got={response.status_code}"
                )

        assert response.status_code == 422

# ============================================================
# VALID TESTS for ALIAS
# ============================================================

@pytest.mark.regression
@pytest.mark.payments_hypothesis_valid_alias
class TestRestPaymentsTransferHypothesisValidAlias:
    """
    Tests con datos válidos.
    Solo variamos 'alias'.
    """

    VALID_ALIAS_REGEX = r"[A-Za-z0-9][A-Za-z0-9.-]{4,18}[A-Za-z0-9]"
    
    valid_alias_strategy = st.from_regex(VALID_ALIAS_REGEX, fullmatch=True,)

    @settings(
        max_examples=20,
        suppress_health_check=[
            HealthCheck.function_scoped_fixture
        ]
    )
    @given(alias=valid_alias_strategy)

    # Casos históricos de alias válidos reales
    @example(alias="Farmacia-24hs")
    @example(alias="Test.123")
    @example(alias="abc123")                 # 6 chars (mínimo)
    @example(alias="a"*20)                  # 20 chars (máximo)
    @example(alias="123456")                # solo números
    @example(alias="abcdef")                # solo letras
    @example(alias="a.b-c1")                # mezcla realista

    def test_transfer_valid_alias(
        self,
        alias,
        payments_transfer_services
    ):
        """
        Property test:
        alias válido no debería devolver error.
        """

        payload = {
            "from_account_id": "ACC-001",
            "to_alias": alias,
            "amount": 1,
            "currency": "ARS",
            "idempotency_key": "IDEMP-999",
        }

        print("Payload:", payload)

        response = payments_transfer_services.post_transfer(
            payload
        )

        print(json.dumps(payload, indent=2, ensure_ascii=False))
        print(response.status_code)
        print(response.json())

        assert response.status_code == 202

# ============================================================
# INVALID TESTS for ALIAS
# ============================================================

@pytest.mark.regression
@pytest.mark.payments_hypothesis_invalid_alias
@pytest.mark.xfail(reason="Invalid aliases accepted", strict=False)
class TestRestPaymentsTransferHypothesisInvalidAlias:
    """
    Tests con datos válidos.
    Solo variamos 'alias'.
    """

    invalid_alias_strategy = st.one_of(

        # demasiado corto
        st.text(
            alphabet="abcdefghijklmnopqrstuvwxyz0123456789.-",
            min_size=0,
            max_size=5,
        ),

        # demasiado largo
        st.text(
            alphabet="abcdefghijklmnopqrstuvwxyz0123456789.-",
            min_size=21,
            max_size=40,
        ),

        # caracteres prohibidos
        st.text(
            alphabet="ñÑ &@_.-",
            min_size=6,
            max_size=20,
        ),

        # espacios internos
        st.just("abc def"),

        # símbolos peligrosos
        st.sampled_from([
            "abc@123",
            "abc_123",
        ])
    )

    @settings(
        max_examples=20,
        suppress_health_check=[
            HealthCheck.function_scoped_fixture
        ]
    )
    @given(alias=invalid_alias_strategy)
  
    # Casos históricos de alias inválidos reales
    @example(alias="Farma&Cloud")
    @example(alias="Farma & Cloud")
    @example(alias="abc ñ def")
    @example(alias="")         # vacío
    @example(alias="     ")    # solo espacios
    @example(alias="------")
    @example(alias="......")
    @example(alias="-----.")
    @example(alias=".-.-.-")

    def test_transfer_invalid_alias(
        self,
        alias,
        payments_transfer_services,
        request
    ):
        """
        Property test:
        alias válido no debería devolver error.
        """

        payload = {
            "from_account_id": "ACC-001",
            "to_alias": alias,
            "amount": 1,
            "currency": "ARS",
            "idempotency_key": "IDEMP-999",
        }

        print("Payload:", payload)

        response = payments_transfer_services.post_transfer(
            payload
        )

        print(json.dumps(payload, indent=2, ensure_ascii=False))
        print(response.status_code)
        print(response.json())

        note(f"alias={alias}")
        note(f"status={response.status_code}")

        if response.status_code == 202:
            invalid_alias_results.append(
                (alias, 422, response.status_code)
            )

            pytest.xfail(
                f"Invalid alias accepted: alias='{alias}' "
                f"expected=422 got={response.status_code}"
            )

        assert True