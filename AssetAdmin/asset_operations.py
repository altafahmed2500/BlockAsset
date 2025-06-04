from .blockchain_connection import web3, contract
import os


def create_asset(ipfs_hash, asset_name, account_id, private_key_env_var):
    """
    Create a new asset on the blockchain.

    Args:
        ipfs_hash (str): The IPFS hash of the asset.
        asset_name (str): The name of the asset.
        account_id (str): The account address to use for the transaction.
        private_key_env_var (str): The name of the environment variable where the
                                   private key is securely stored.

    Returns:
        dict: The details of the created asset.

    Raises:
        RuntimeError: If the private key cannot be retrieved securely.
    """
    # Retrieve the private key from a secure environment variable
    private_key = os.environ.get(private_key_env_var)
    if private_key is None or not private_key.strip():
        raise RuntimeError("Private key environment variable '{}' not found or is empty.".format(private_key_env_var))

    # Get the nonce for the account
    nonce = web3.eth.get_transaction_count(account_id)

    # Build the transaction
    tx = contract.functions.createToken(ipfs_hash, asset_name).build_transaction({
        'from': account_id,
        'nonce': nonce,
        'gas': 3000000,  # Adjust as needed
        'gasPrice': web3.to_wei('10', 'gwei')
    })

    # Sign the transaction using the private key from secure storage
    signed_tx = web3.eth.account.sign_transaction(tx, private_key)

    # Securely delete private_key variable from memory as soon as possible
    private_key = '0' * len(private_key)
    del private_key

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