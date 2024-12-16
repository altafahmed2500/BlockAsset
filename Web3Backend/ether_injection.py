from web3 import Web3
from .connection_web3 import hardhat_connection_string


def send_ether_to_one(sender_address, sender_private_key, receiver_address, amount_in_ether):
    # Connect to Hardhat
    web3 = hardhat_connection_string()

    # Convert Ether to Wei
    amount_in_wei = web3.to_wei(amount_in_ether, 'ether')

    # Get the nonce
    nonce = web3.eth.get_transaction_count(sender_address)

    # Create the transaction
    transaction = {
        'to': receiver_address,
        'value': amount_in_wei,
        'gas': 21000,  # Standard gas limit for Ether transfer
        'gasPrice': web3.to_wei('20', 'gwei'),
        'nonce': nonce,
        'chainId': 31337  # Hardhat's default chain ID
    }

    # Sign the transaction
    signed_txn = web3.eth.account.sign_transaction(transaction, private_key=sender_private_key)

    # Send the transaction
    tx_hash = web3.eth.send_raw_transaction(signed_txn.raw_transaction)

    return tx_hash.hex()  # Return the transaction hash as a hex string
