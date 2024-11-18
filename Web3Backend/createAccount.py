from web3 import Web3

ganache_url = "http://127.0.0.1:7545"
web3 = Web3(Web3.HTTPProvider(ganache_url))


# Check if the connection is successful
if not web3.isConnected():
    raise Exception("Unable to connect to Ganache")

