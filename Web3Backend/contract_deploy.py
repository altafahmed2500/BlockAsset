from web3 import Web3
from solcx import compile_standard, install_solc, set_solc_version


def deploy_contract(connection_string, abi, bytecode, owner_private_key):
    try:
        # Connect to Ganache
        account = connection_string.eth.account.from_key(owner_private_key)
        print(f"Deploying contract from address: {account.address}")

        # Get chain ID dynamically
        chain_id = connection_string.eth.chain_id
        print(f"Using chain ID: {chain_id}")

        # Create contract instance
        contract = connection_string.eth.contract(abi=abi, bytecode=bytecode)

        # Estimate gas
        estimated_gas = contract.constructor().estimate_gas({"from": account.address})
        print(f"Estimated gas: {estimated_gas}")

        # Build the deployment transaction
        transaction = contract.constructor().build_transaction({
            "chainId": chain_id,
            "gas": estimated_gas,  # Add buffer
            "gasPrice": connection_string.to_wei("20", "gwei"),
            "nonce": connection_string.eth.get_transaction_count(account.address),
        })

        # Sign and send the transaction
        print("Signing and sending the transaction...")
        signed_txn = connection_string.eth.account.sign_transaction(transaction, owner_private_key)
        txn_hash = connection_string.eth.send_raw_transaction(signed_txn.raw_transaction)
        print(f"Transaction hash: {txn_hash.hex()}")

        # Wait for transaction receipt
        txn_receipt = connection_string.eth.wait_for_transaction_receipt(txn_hash)
        print(f"Contract deployed at address: {txn_receipt.contractAddress}")

        # Verify the contract deployment
        deployed_contract = connection_string.eth.contract(address=txn_receipt.contractAddress, abi=abi)
        if deployed_contract:
            print("Contract verified successfully.")

        return txn_receipt.contractAddress

    except ValueError as ve:
        if "exceeds gas limit" in str(ve):
            print("Error: Gas limit exceeded. Increase the gas limit.")
        else:
            print(f"ValueError: {ve}")
    except Exception as e:
        print(f"Error during deployment: {e}")
        return None
