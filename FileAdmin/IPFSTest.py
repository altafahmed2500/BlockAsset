import requests

def add_file_to_ipfs(file_path):
    """
    Add a file to IPFS using HTTP API.
    """
    url = "http://127.0.0.1:5001/api/v0/add"
    try:
        with open(file_path, 'rb') as file:
            files = {'file': file}
            response = requests.post(url, files=files)
            response.raise_for_status()
            return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error adding file to IPFS: {e}")
        return None

# Example usage
file_path = '../media/uploads/Ahmed_Altaf.pdf'
result = add_file_to_ipfs(file_path)
if result:
    print("File added to IPFS:", result)
