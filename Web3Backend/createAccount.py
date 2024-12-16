from web3 import Web3

# URL for Hardhat's local development network
hardhat_url = "http://127.0.0.1:8545"
web3 = Web3(Web3.HTTPProvider(hardhat_url))

# Check if the connection is successful
if not web3.isConnected():
    raise Exception("Unable to connect to Hardhat")

print("Connected to Hardhat successfully!")
