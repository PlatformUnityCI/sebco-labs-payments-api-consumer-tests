@regression
@payments_copy
Feature: Payments Transfers

    Background:
        Given el storage de transferencias está vacío
        And existe un payload base de transferencia válido

    Scenario: Crear una transferencia válida
        When envío la transferencia
        Then el status code es 202
        And el estado de la transferencia es "PENDING"
        And los datos de la transferencia son correctos
        And el transfer_id es válido
        And la transferencia se guarda en storage

    Scenario Outline: Validar creación de transferencias con límites de amount
        Given modifico el amount a "<amount>"
        When envío la transferencia
        Then el status code es <status>
        And el error contiene el tipo "<error_type>"

        Examples:
            | amount  | status | error_type   |
            | 250.0   | 202    | none         |
            | 0.01    | 202    | none         |
            | 0       | 422    | greater_than |
            | -10     | 422    | greater_than |
            | -0.01   | 422    | greater_than |
            | 1000000 | 202    | none         |

    Scenario Outline: Validar creación de transferencias con tipos inválidos de amount
        Given modifico el amount a "<amount>"
        When envío la transferencia
        Then el status code es <status>

        Examples:
            | amount | status | error_type    |
            | abc    | 422    | float_parsing |
            | None   | 422    | float_type    |
            | null   | 422    | none          |
            | [100]  | 422    | float_type    |

    Scenario Outline: Validar creación de transferencias con coerción de tipos en amount
        Given modifico el amount a "<amount>"
        When envío la transferencia
        Then el status code es <status>

        Examples:
            | amount | status | error_type |
            | true   | 202    | none       |

    Scenario: Validar creación de transferencias con comillas internas inválido en amount
        Given modifico el amount a "\"100\""
        When envío la transferencia
        Then el status code es 422