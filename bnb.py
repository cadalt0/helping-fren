import requests
import sys

def get_bnb_transaction(tx_id):
    url = "https://bsc-dataseed.binance.org:443"
    payload = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "eth_getTransactionByHash",
        "params": [tx_id]
    }
    headers = {"Content-Type": "application/json"}

    response = requests.post(url, json=payload, headers=headers)

    if response.status_code == 200:
        data = response.json()
        return data.get("result", "No result found.")
    else:
        return f"Error fetching data: {response.status_code}"

if __name__ == "__main__":
    tx_id = sys.argv[1]
    print(get_bnb_transaction(tx_id))
