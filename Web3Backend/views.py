from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from .contract_compile import contract_compilation
from .connection_web3 import ganache_connection_string
from .contract_deploy import deploy_contract
from UserAdmin.permisssion import IsAdminUser
from .ether_injection import send_ether_to_one
from .ether_balance import check_account_balance


@api_view(['POST'])
@permission_classes([IsAdminUser])
def admin_ether_push(request):
    # Extract required fields from request data
    sender_private_key = request.data.get("sender_private_key")
    sender_address = request.data.get("sender_address")
    receiver_address = request.data.get("receiver_address")
    amount_in_ether = request.data.get("amount_in_ether")

    # Validate the inputs
    if not (sender_private_key and sender_address and receiver_address and amount_in_ether):
        return Response({
            "error": "All fields are required (sender_private_key, sender_address, receiver_address, amount_in_ether)"},
            status=400)

    try:
        # Send Ether using utility function
        tx_hash = send_ether_to_one(sender_address, sender_private_key, receiver_address, float(amount_in_ether))
        return Response({"message": "Transaction sent successfully", "transaction_hash": tx_hash}, status=200)
    except Exception as e:
        return Response({"error": str(e)}, status=500)


@api_view(['GET'])
@permission_classes([IsAdminUser])
def admin_ether_balance(request):
    # Extract required fields from request data
    address = request.data.get("address")

    if not address:
        return Response({
            "error": "All fields are required addresss"},
            status=400)

    try:
        # Send Ether using utility function

        balance = check_account_balance(address)
        return Response({"message": "Transaction sent successfully", "balance": balance}, status=200)
    except Exception as e:
        return Response({"error": str(e)}, status=500)


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
