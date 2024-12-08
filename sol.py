import re
import requests
import threading

# Define the Helius RPC endpoint URL and API key
HELIUS_RPC_URL = "https://mainnet.helius-rpc.com/?api-key=cb83df62-cfa5-4cec-92ee-b2bf72c34dba"

# Specify the target group/channel ID
TARGET_GROUP_ID = -1002444698070  # Replace with your actual target group ID

# Function to fetch transaction details from Solana using Helius RPC
def get_sol_transaction_details(tx_id):
    try:
        # Define the request payload for Helius RPC
        payload = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "getTransaction",
            "params": [tx_id]
        }

        # Send the request to Helius RPC
        response = requests.post(HELIUS_RPC_URL, json=payload)

        # Check if the response was successful
        if response.status_code == 200:
            data = response.json()

            # Check if the transaction details were retrieved
            if "result" in data and data["result"]:
                return data["result"]
            else:
                return {"error": "Transaction not found or invalid TX ID"}
        else:
            return {"error": "Failed to fetch data from Helius RPC"}
    except Exception as e:
        return {"error": str(e)}

# Function to process incoming messages
def process_message(message, bot):
    """
    Processes a message, checks for 20+ character alphanumeric strings,
    and fetches Solana transaction details if found.

    :param message: The incoming message content.
    :param bot: The bot instance for sending messages.
    """
    # Look for alphanumeric strings of 20+ characters (letters + numbers)
    tx_hash_match = re.search(r"\b[a-zA-Z0-9]{20,}\b", message)

    if tx_hash_match:
        tx_id = tx_hash_match.group(0)
        bot.send_message(message.chat.id, "Working on it...")  # Notify user that processing started

        # Use a separate thread to fetch details and respond
        def background_fetch():
            details = get_sol_transaction_details(tx_id)
            if 'error' in details:
                bot.send_message(message.chat.id, f"Error: {details['error']}")
            else:
                bot.send_message(message.chat.id, f"Transaction Details: {details}")

        threading.Thread(target=background_fetch).start()

def register(bot):
    """
    Registers the Solana transaction handler with the bot.
    
    :param bot: The bot instance to attach the handler to.
    """
    @bot.message_handler(func=lambda message: True)  # Capture all messages
    def handle_message(message):
        process_message(message.text, bot)  # Process incoming message


# import requests

# # Define the Helius RPC endpoint URL and API key
# HELIUS_RPC_URL = "https://mainnet.helius-rpc.com/?api-key=cb83df62-cfa5-4cec-92ee-b2bf72c34dba"

# def get_sol_transaction_details(tx_id):
#     try:
#         # Define the request payload for Helius RPC
#         payload = {
#             "jsonrpc": "2.0",
#             "id": 1,
#             "method": "getTransaction",
#             "params": [tx_id]
#         }

#         # Send the request to Helius RPC
#         response = requests.post(HELIUS_RPC_URL, json=payload)

#         # Check if the response was successful
#         if response.status_code == 200:
#             data = response.json()

#             # Check if the transaction details were retrieved
#             if "result" in data and data["result"]:
#                 return data["result"]
#             else:
#                 return {"error": "Transaction not found or invalid TX ID"}
#         else:
#             return {"error": "Failed to fetch data from Helius RPC"}
#     except Exception as e:
#         return {"error": str(e)}
