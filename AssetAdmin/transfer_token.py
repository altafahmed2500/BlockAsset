from .blockchain_connection import web3, contract


def transfer_token(token_id, to_address, account_id, private_key):
    """
    Transfer a token to another address.

    Args:
        token_id (int): The ID of the token to transfer.
        to_address (str): The recipient's Ethereum address.
        account_id (str): The sender's Ethereum address.
        private_key (str): The private key of the sender.

    Returns:
        dict: The transaction details.
    """
    # Get the nonce for the sender's account
    nonce = web3.eth.get_transaction_count(account_id)

    # Build the transaction
    tx = contract.functions.transferToken(token_id, to_address).build_transaction({
        'from': account_id,
        'nonce': nonce,
        'gas': 3000000,  # Adjust gas limit as needed
        'gasPrice': web3.to_wei('10', 'gwei')
    })

    # Sign the transaction
    signed_tx = web3.eth.account.sign_transaction(tx, private_key)

    # Send the transaction
    tx_hash = web3.eth.send_raw_transaction(signed_tx.raw_transaction)

    # Wait for the transaction receipt
    receipt = web3.eth.wait_for_transaction_receipt(tx_hash)

    # Return the transaction details
    return {
        "transaction_id": tx_hash.hex(),
        "block_number": receipt.blockNumber,
        "status": receipt.status,
    }
