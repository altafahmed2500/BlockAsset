from web3 import Web3


def hardhat_connection_string():
    # Connect to local blockchain (Ganache in this example)
    web3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8545"))

    # Check if connection is successful
    if not web3.is_connected():
        raise Exception("Blockchain connection failed")
    return web3
