import json

from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from .contract_compile import contract_compilation
from .connection_web3 import ganache_connection_string
from .contract_deploy import deploy_contract
from UserAdmin.permisssion import IsAdminUser


# @api_view(['GET'])
# def get_


@api_view(['GET'])
@permission_classes([IsAdminUser])
def test_contract(request):
    # Extract the owner_private_address from the request data
    owner_private_address = request.data.get("owner_private_address")
    if not owner_private_address:
        return Response({"error": "owner_private_address is required"}, status=400)

    try:
        # Compile the contract to get ABI and bytecode
        abi, bytecode = contract_compilation()

        # Check if ABI and bytecode are valid
        if not isinstance(abi, list):
            return Response({"error": "ABI must be a list of dictionaries."}, status=400)
        if not isinstance(bytecode, str):
            return Response({"error": "Bytecode must be a string."}, status=400)

        # Deploy the contract using the Web3 functions
        local_connection_string = ganache_connection_string()
        contract_address = deploy_contract(local_connection_string, abi, bytecode, owner_private_address)

        # Return the deployed contract address
        return Response({"message": f"The deployed contract details are {contract_address}"})

    except Exception as e:
        # Handle and log errors
        return Response({"error": f"Deployment failed: {str(e)}"}, status=500)
