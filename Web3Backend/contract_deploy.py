def deploy_contract(connection_string, abi, bytecode, owner_private_address):
    # Create the contract instance
    account = connection_string.eth.account.from_key(owner_private_address)
    print(account.address)
    contract_storage = connection_string.eth.contract(abi=abi, bytecode=bytecode)
    # Build the deployment transaction
    transaction = contract_storage.constructor("42").build_transaction({
        "chainId": 1337,  # Ganache default chain ID
        "gas": 3000000,
        "gasPrice": connection_string.to_wei("20", "gwei"),
        "nonce": connection_string.eth.get_transaction_count("0x1712A2DE30dd4c34a52701878eD7239accF14f77"),
        # "nonce": connection_string.eth.get_transaction_count(account.address),
    })

    # Sign and send the transaction
    # private_key = owner_private_address
    private_key = "0xaee977f0590627d1c0f6af13f036f91e644d6bd75313a275c169aeec20aa9167"
    # Replace with your private key
    signed_txn = connection_string.eth.account.sign_transaction(transaction, private_key)
    txn_hash = connection_string.eth.send_raw_transaction(signed_txn.raw_transaction)

    # Wait for transaction receipt
    txn_receipt = connection_string.eth.wait_for_transaction_receipt(txn_hash)

    # Output deployed contract address
    print(f"Contract deployed at address: {txn_receipt.contractAddress}")
    return txn_receipt.contractAddress
