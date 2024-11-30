import os
from solcx import compile_standard, install_solc
import json

# Install Solidity compiler
install_solc("0.8.0")

# Get the absolute path of node_modules
current_dir = os.getcwd()  # Current working directory
node_modules_path = os.path.abspath(os.path.join(current_dir, "node_modules"))  # Absolute path

# Print to verify
print("Node Modules Path:", node_modules_path)

# Load the Solidity file
with open("NFTMinting.sol", "r") as file:
    contract_source_code = file.read()

# Compile the contract
compiled_sol = compile_standard(
    {
        "language": "Solidity",
        "sources": {"NFTMinting.sol": {"content": contract_source_code}},
        "settings": {
            "outputSelection": {
                "*": {
                    "*": ["abi", "metadata", "evm.bytecode", "evm.sourceMap"]
                }
            }
        },
    },
    solc_version="0.8.0",
    allow_paths=node_modules_path,  # Pass absolute path
)

# Save compiled data
with open("compiled_code.json", "w") as file:
    json.dump(compiled_sol, file)

# Extract ABI and Bytecode
abi = compiled_sol["contracts"]["NFTMinting.sol"]["NFTMinting"]["abi"]
bytecode = compiled_sol["contracts"]["NFTMinting.sol"]["NFTMinting"]["evm"]["bytecode"]["object"]
