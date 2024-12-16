from .blockchain_connection import web3, contract


def create_asset(ipfs_hash, asset_name, account_id, private_key):
    """
    Create a new asset on the blockchain.

    Args:
        ipfs_hash (str): The IPFS hash of the asset.
        asset_name (str): The name of the asset.
        account_id (str): The account address to use for the transaction.
        private_key (str): The private key of the account.

    Returns:
        dict: The details of the created asset.
    """
    # Get the nonce for the account
    nonce = web3.eth.get_transaction_count(account_id)

    # Build the transaction
    tx = contract.functions.createToken(ipfs_hash, asset_name).build_transaction({
        'from': account_id,
        'nonce': nonce,
        'gas': 3000000,  # Adjust as needed
        'gasPrice': web3.to_wei('10', 'gwei')
    })

    # Sign the transaction
    signed_tx = web3.eth.account.sign_transaction(tx, private_key)

    # Send the transaction
    tx_hash = web3.eth.send_raw_transaction(signed_tx.raw_transaction)

    # Wait for the transaction receipt
    receipt = web3.eth.wait_for_transaction_receipt(tx_hash)

    # Process the event log for TokenCreated
    event = contract.events.TokenCreated().process_receipt(receipt)[0]['args']

    # Return the asset creation details
    return {
        "transaction_id": tx_hash.hex(),
        "block_number": receipt.blockNumber,
        "token_id": event["tokenId"],
        "owner": event["owner"],
        "ipfs_hash": ipfs_hash,
        "name": asset_name
    }
