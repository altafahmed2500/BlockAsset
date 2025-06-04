from web3 import Web3
import os

# Connect to the local Ethereum network
provider_url = "http://127.0.0.1:8545"  # Hardhat local node
web3 = Web3(Web3.HTTPProvider(provider_url))

# Check connection
if not web3.is_connected():
    raise ConnectionError("Failed to connect to Ethereum node.")

# Contract details
contract_address = "0xe7f1725E7734CE288F8367e1Bb143E90bb3F0512"  # Replace with the deployed contract address
contract_abi = [
    {
        "inputs": [
            {
                "internalType": "string",
                "name": "_name",
                "type": "string"
            },
            {
                "internalType": "string",
                "name": "_symbol",
                "type": "string"
            }
        ],
        "stateMutability": "nonpayable",
        "type": "constructor"
    },
    {
        "anonymous": False,
        "inputs": [
            {
                "indexed": False,
                "internalType": "uint256",
                "name": "tokenId",
                "type": "uint256"
            },
            {
                "indexed": False,
                "internalType": "string",
                "name": "ipfsHash",
                "type": "string"
            },
            {
                "indexed": False,
                "internalType": "string",
                "name": "name",
                "type": "string"
            },
            {
                "indexed": False,
                "internalType": "address",
                "name": "owner",
                "type": "address"
            }
        ],
        "name": "TokenCreated",
        "type": "event"
    },
    {
        "anonymous": False,
        "inputs": [
            {
                "indexed": False,
                "internalType": "uint256",
                "name": "tokenId",
                "type": "uint256"
            },
            {
                "indexed": False,
                "internalType": "address",
                "name": "from",
                "type": "address"
            },
            {
                "indexed": False,
                "internalType": "address",
                "name": "to",
                "type": "address"
            }
        ],
        "name": "TokenTransferred",
        "type": "event"
    },
    {
        "inputs": [
            {
                "internalType": "address",
                "name": "_owner",
                "type": "address"
            }
        ],
        "name": "balanceOf",
        "outputs": [
            {
                "internalType": "uint256",
                "name": "",
                "type": "uint256"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "string",
                "name": "_ipfsHash",
                "type": "string"
            },
            {
                "internalType": "string",
                "name": "_assetName",
                "type": "string"
            }
        ],
        "name": "createToken",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "uint256",
                "name": "_tokenId",
                "type": "uint256"
            }
        ],
        "name": "getIPFSHash",
        "outputs": [
            {
                "internalType": "string",
                "name": "",
                "type": "string"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "uint256",
                "name": "_tokenId",
                "type": "uint256"
            }
        ],
        "name": "getTokenName",
        "outputs": [
            {
                "internalType": "string",
                "name": "",
                "type": "string"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [],
        "name": "name",
        "outputs": [
            {
                "internalType": "string",
                "name": "",
                "type": "string"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "uint256",
                "name": "_tokenId",
                "type": "uint256"
            }
        ],
        "name": "ownerOf",
        "outputs": [
            {
                "internalType": "address",
                "name": "",
                "type": "address"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [],
        "name": "symbol",
        "outputs": [
            {
                "internalType": "string",
                "name": "",
                "type": "string"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [],
        "name": "totalTokens",
        "outputs": [
            {
                "internalType": "uint256",
                "name": "",
                "type": "uint256"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "uint256",
                "name": "_tokenId",
                "type": "uint256"
            },
            {
                "internalType": "address",
                "name": "_to",
                "type": "address"
            }
        ],
        "name": "transferToken",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    }
]

# Initialize the contract
contract = web3.eth.contract(address=contract_address, abi=contract_abi)

# Retrieve private key from environment variable
private_key = os.environ.get("ETH_PRIVATE_KEY")
if private_key is None:
    raise EnvironmentError("Environment variable ETH_PRIVATE_KEY is not set.")

# Retrieve account address from private key
try:
    account_obj = web3.eth.account.from_key(private_key)
    account_id = account_obj.address
except Exception as e:
    raise ValueError("Invalid private key provided in ETH_PRIVATE_KEY environment variable.") from e


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
        "token_id": event["tokenId"],
        "owner": event["owner"],
        "ipfs_hash": ipfs_hash,
        "name": asset_name
    }


ipfs_hash = "QmSQzzZThcLhFSwqge9w9PmUJJ2SgzTqb8q2wVLvfjUo3G"
asset_name = "sample"
create_asset(ipfs_hash, asset_name, account_id, private_key)