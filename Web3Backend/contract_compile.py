import os
import json
from solcx import compile_standard, install_solc, set_solc_version
from solcx import install_solc, set_solc_version

install_solc('0.8.20')
set_solc_version('0.8.20')


def contract_compilation():
    try:
        # Install and set the correct compiler version
        install_solc('0.8.20')
        set_solc_version('0.8.20')

        # Directory containing Solidity contracts
        contracts_directory = os.path.abspath("C:/Users/altaf/Desktop/Block-Assets-API/BlockAsset/media/contracts")

        # Specific contract file to compile
        contract_file = os.path.join(contracts_directory, "NFTMinting.sol")

        # Read the Solidity file
        with open(contract_file, "r") as file:
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
            solc_version="0.8.20",
            allow_paths=f"{contracts_directory};{contracts_directory}/node_modules"
        )

        # Save compiled contract to file (optional)
        with open("compiled_code.json", "w") as file:
            json.dump(compiled_sol, file)

        # Extract ABI and bytecode
        abi = compiled_sol["contracts"]["NFTMinting.sol"]["NFTMinting"]["abi"]
        bytecode = compiled_sol["contracts"]["NFTMinting.sol"]["NFTMinting"]["evm"]["bytecode"]["object"]
        print("compilation Completed")
        print(abi)
        return (abi, bytecode)

    except Exception as e:
        print(f"Error during contract compilation: {e}")
        return None, None
