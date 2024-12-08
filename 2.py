import requests

# Define the Helius API URL and your API key
API_URL = "https://mainnet.helius-rpc.com/"
API_KEY = "cb83df62-cfa5-4cec-92ee-b2bf72c34dba"  # Replace with your actual API key

# Function to fetch transaction details using the getTransaction method
def fetch_transaction(x_id):
    headers = {
        "Authorization": f"Bearer {API_KEY}"
    }
    params = {
        "transactionId": x_id  # The parameter for transaction ID
    }

    # Send a GET request to the Helius API
    response = requests.get(f"{API_URL}/getTransaction", headers=headers, params=params)

    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: {response.status_code}")
        return None

# Main program to ask for the transaction ID and fetch details
def main():
    x_id = input("Please enter the transaction ID: ")

    # Fetch transaction details from the Helius API
    transaction_data = fetch_transaction(x_id)

    if transaction_data:
        # Print the fetched transaction data in the terminal
        print("\nFetched Transaction Data:")
        print(transaction_data)

if __name__ == "__main__":
    main()
