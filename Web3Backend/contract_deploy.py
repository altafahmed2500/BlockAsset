from web3 import Web3
from solcx import compile_standard, install_solc, set_solc_version


def deploy_contract(connection_string, abi, bytecode, owner_private_key):
    try:
        # Connect to Ganache
        account = connection_string.eth.account.from_key(owner_private_key)
        print(f"Deploying contract from address: {account.address}")

        # Create contract instance
        contract = connection_string.eth.contract(abi=abi, bytecode=bytecode)

        # Estimate gas
        estimated_gas = contract.constructor().estimate_gas({"from": account.address})

        # Build the deployment transaction
        transaction = contract.constructor().build_transaction({
            "chainId": 5777,  # Use Ganache's Network ID
            "gas": estimated_gas + 50000,
            "gasPrice": connection_string.to_wei("10", "gwei"),
            "nonce": connection_string.eth.get_transaction_count(account.address),
        })

        # Sign and send the transaction
        signed_txn = connection_string.eth.account.sign_transaction(transaction, owner_private_key)
        txn_hash = connection_string.eth.send_raw_transaction(signed_txn.raw_transaction)

        # Wait for transaction receipt
        txn_receipt = connection_string.eth.wait_for_transaction_receipt(txn_hash)
        print(f"Contract deployed at address: {txn_receipt.contractAddress}")

        return txn_receipt.contractAddress

    except Exception as e:
        print(f"Error during deployment: {e}")
        return None
