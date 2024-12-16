# Function to check account balance
from .connection_web3 import hardhat_connection_string


def check_account_balance(account_address):
    web3 = hardhat_connection_string()
    try:
        # Validate address
        if not web3.is_address(account_address):
            return f"Invalid Ethereum address: {account_address}"

        # Get balance in Wei
        balance_wei = web3.eth.get_balance(account_address)

        # Convert Wei to Ether
        balance_ether = web3.from_wei(balance_wei, 'ether')
        return balance_ether
    except Exception as e:
        return f"Error: {str(e)}"
