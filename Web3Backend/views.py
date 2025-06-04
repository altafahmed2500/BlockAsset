from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from .contract_compile import contract_compilation
from .connection_web3 import hardhat_connection_string
from .contract_deploy import deploy_contract
from UserAdmin.permisssion import IsAdminUser
from .ether_injection import send_ether_to_one
from .ether_balance import check_account_balance
from AccountAdmin.models import AccountProfile

web3 = hardhat_connection_string()


def _is_request_secure(request):
    """
    Returns True if the request was made securely (over HTTPS).
    Handles common reverse proxy scenarios.
    """
    if request.is_secure():
        return True
    # Handle 'X-Forwarded-Proto' for deployments behind reverse proxy
    x_forwarded_proto = request.META.get('HTTP_X_FORWARDED_PROTO')
    if x_forwarded_proto:
        return x_forwarded_proto == 'https'
    return False


@api_view(['POST'])
@permission_classes([IsAdminUser])
def admin_ether_push_allusers(request):
    # Enforce HTTPS/TLS for sensitive credential submission
    if not _is_request_secure(request):
        return Response(
            {"error": "Insecure transport: This endpoint requires HTTPS/TLS for all requests due to handling sensitive credentials."},
            status=403
        )

    try:
        # Establish connection to Hardhat blockchain
        web3 = hardhat_connection_string()

        # Get sender's private key from request
        sender_private_key = request.data.get("sender_private_key")
        if not sender_private_key:
            return Response({"error": "Sender private key is required."}, status=400)

        # Get the first account from Hardhat as the sender address
        accounts = web3.eth.accounts
        if not accounts:
            return Response({"error": "No accounts available in Hardhat."}, status=500)
        sender_address = accounts[0]

        # Convert to Wei (10 Ether)
        amount_in_wei = web3.to_wei(10, 'ether')

        # Fetch all accounts in AccountProfile
        account_profiles = AccountProfile.objects.all()
        if not account_profiles.exists():
            return Response({"error": "No accounts found in AccountProfile."}, status=404)

        transaction_hashes = []

        for account in account_profiles:
            receiver_address = account.public_address
            if not receiver_address:
                continue

            # Build the transaction
            transaction = {
                'from': sender_address,
                'to': receiver_address,
                'value': amount_in_wei,
                'gas': 21000,
                'gasPrice': web3.to_wei('20', 'gwei'),
                'nonce': web3.eth.get_transaction_count(sender_address),
            }

            # Sign the transaction with the private key from the request
            signed_tx = web3.eth.account.sign_transaction(transaction, sender_private_key)

            # Send the transaction
            tx_hash = web3.eth.send_raw_transaction(signed_tx.raw_transaction)
            transaction_hashes.append(web3.to_hex(tx_hash))

        return Response({
            "message": "Ether sent successfully to all accounts.",
            "transaction_hashes": transaction_hashes
        }, status=200)

    except Exception as e:
        return Response({"error": str(e)}, status=500)


@api_view(['POST'])
@permission_classes([IsAdminUser])
def admin_ether_push(request):
    # Enforce HTTPS/TLS for sensitive credential submission
    if not _is_request_secure(request):
        return Response(
            {"error": "Insecure transport: This endpoint requires HTTPS/TLS for all requests due to handling sensitive credentials."},
            status=403
        )

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
    # No sensitive input; no HTTPS enforcement needed here
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