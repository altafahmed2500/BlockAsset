from solcx import install_solc, compile_standard
import json

install_solc("0.8.0")


def contract_compilation():
    contract_file = "C:/Users/altaf/Desktop/Block-Assets-API/BlockAsset/media/contract/TestCode.sol"
    # Read the Solidity file
    with open(contract_file, "r") as file:
        contract_source_code = file.read()

    # Compile the contract
    compiled_sol = compile_standard(
        {
            "language": "Solidity",
            "sources": {"TestCode.sol": {"content": contract_source_code}},
            "settings": {
                "outputSelection": {
                    "*": {
                        "*": ["abi", "metadata", "evm.bytecode", "evm.sourceMap"]
                    }
                }
            },
        },
        solc_version="0.8.0",
    )

    # Save compiled contract to file (optional)
    with open("compiled_code.json", "w") as file:
        json.dump(compiled_sol, file)

    # Extract ABI and bytecode
    abi = compiled_sol["contracts"]["TestCode.sol"]["TestCode"]["abi"]
    bytecode = compiled_sol["contracts"]["TestCode.sol"]["TestCode"]["evm"]["bytecode"]["object"]
    return (abi, bytecode)

# web3 = ganache_connection_string()
