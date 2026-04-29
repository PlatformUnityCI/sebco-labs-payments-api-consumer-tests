from hypothesis import strategies as st


transfer_strategy = st.fixed_dictionaries({

    "from_account_id": st.sampled_from([
        "ACC-001"
    ]),

    "to_alias": st.sampled_from([
        "alias.destino"
    ]),

    "amount": st.integers(
        min_value=1,
        max_value=1_000_000
    ),

    "currency": st.just("ARS"),

    "idempotency_key": st.from_regex(
        r"^IDEMP-[0-9]{3,6}$",
        fullmatch=True
    )
})