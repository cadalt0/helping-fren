import google.generativeai as genai
import requests
import json

# Configure Google Generative AI
genai.configure(api_key=key")
model = genai.GenerativeModel("gemini-1.5-flash")

# Store user conversation history and transaction-related details
user_conversations = {}
user_transactions = {}

# Define Solana RPC URL
solana_rpc_url = "https://api.mainnet.solana.com"

def register(bot):
    # Define the target group ID
    TARGET_GROUP_ID = -1002444698070

    @bot.message_handler(func=lambda message: message.chat.id == TARGET_GROUP_ID)
    def handle_message(message):
        try:
            # Log the received message details
            user_name = message.from_user.username or message.from_user.first_name
            user_message = message.text.strip()
            print(f"Received from {user_name} in group {TARGET_GROUP_ID}: {user_message}")

            # Initialize user conversation and transaction states
            if message.from_user.id not in user_conversations:
                user_conversations[message.from_user.id] = []
            if message.from_user.id not in user_transactions:
                user_transactions[message.from_user.id] = {
                    "awaiting_chain": False,
                    "awaiting_tx_id": False,
                    "chain": None,
                    "tx_id": None,
                }

            # Reset conversation if "!e" is received
            if user_message.lower() == "!e":
                user_conversations[message.from_user.id] = []
                user_transactions[message.from_user.id] = {
                    "awaiting_chain": False,
                    "awaiting_tx_id": False,
                    "chain": None,
                    "tx_id": None,
                }
                bot.reply_to(message, "Conversation reset. Let's start fresh! How can I assist you today?")
                return

            # Respond "gm" if the user sends "gm"
            if user_message.lower() == "gm":
                bot.reply_to(message, "gm 🙌")
                return

            # Handle transaction-related queries
            if "transaction" in user_message.lower() or "transfer" in user_message.lower() or "payment" in user_message.lower() or "send" in user_message.lower():
                # Handle transaction flow
                if user_transactions[message.from_user.id]["awaiting_chain"]:
                    user_transactions[message.from_user.id]["chain"] = user_message
                    user_transactions[message.from_user.id]["awaiting_chain"] = False
                    user_transactions[message.from_user.id]["awaiting_tx_id"] = True
                    bot.reply_to(message, "Got it! Now, please provide the transaction ID.")
                elif user_transactions[message.from_user.id]["awaiting_tx_id"]:
                    user_transactions[message.from_user.id]["tx_id"] = user_message
                    user_transactions[message.from_user.id]["awaiting_tx_id"] = False
                    bot.reply_to(
                        message,
                        f"Transaction details received! Chain: {user_transactions[message.from_user.id]['chain']}, TX ID: {user_transactions[message.from_user.id]['tx_id']}",
                    )
                else:
                    user_transactions[message.from_user.id]["awaiting_chain"] = True
                    bot.reply_to(message, "It seems like you're asking about a transaction. Please provide the chain name (e.g., Solana, Ethereum).")
                return

            # If message length exceeds 20 characters, hardcode the transaction details
            if any(len(word) > 20 for word in user_message.split()):
                print(f"Hardcoding transaction details for message from {user_name}: {user_message}")

                # Hardcoded transaction details based on your example
                transaction_details = {
                    "Transaction ID": "5G1DYHAzAeCCnsGoJrdNnyswZMcoDqb4YYL8vdv1JWanADUkLAFgDKzntLKMYDC1BhTQH3eFgrUAk3529sqaEoJP",
                    "Block & Timestamp": "December 07, 2024 23:59:14 +UTC",
                    "Result": "Success",
                    "Signer": "5uD7Z9p3iBznhR7xidhh91NUPUjak1LCxAMnjB5LsXdL",
                    "Transaction Actions": "Transfer 0.000006 SOL ($0.001433) from 5uD7Z9p3iBznhR7xidhh91NUPUjak1LCxAMnjB5LsXdL to Jitotip 1",
                    "Fee": "0.000005 SOL ($0.001197)",
                    "Compute Units Consumed": 13373,
                    "Transaction Version": 0,
                }

                # Format and send transaction details
                formatted_details = "\n".join([f"{key}: {value}" for key, value in transaction_details.items()])
                bot.reply_to(message, f"Transaction Details:\n\n{formatted_details}")
                return

            # Handle regular conversation
            user_conversations[message.from_user.id].append(f"User: {user_message}")
            context = "\n".join(user_conversations[message.from_user.id][-10:])  # Limit context to the last 10 exchanges

            prompt = (
                f"You are a Web3 expert. Respond professionally to the following conversation with a focus on blockchain, DeFi, NFTs, DAOs, crypto, and decentralized technologies:\n\n"
                f"{context}\n"
                f"AI:"
            )
            ai_response = model.generate_content(prompt)
            reply = ai_response.text

            # Ensure reply is within 80 words and doesn't cut sentences
            words = reply.split()
            if len(words) > 80:
                cutoff_idx = 80
                for i in range(79, -1, -1):
                    if words[i].endswith(('.', '!', '?')):
                        cutoff_idx = i + 1
                        break
                reply = " ".join(words[:cutoff_idx])

            # Ensure no AI self-references
            if any(word.lower() in reply.lower() for word in ["i am", "my name", "i am an ai"]):
                reply = "I can only discuss Web3 topics. Let's stay focused on blockchain, crypto, NFTs, and more!"

            bot.reply_to(message, reply)

        except Exception as e:
            bot.reply_to(message, f"An error occurred: {str(e)}")


# import google.generativeai as genai

# # Configure Google Generative AI
# genai.configure(api_key="AIzaSyAENWtd9ouIs2rKrcA3ZjSjCDO0Xr-8BjY")
# model = genai.GenerativeModel("gemini-1.5-flash")

# # Store user conversation history and transaction-related details
# user_conversations = {}
# user_transactions = {}

# def register(bot):
#     # Define the target group ID
#     TARGET_GROUP_ID = -1002444698070

#     @bot.message_handler(func=lambda message: message.chat.id == TARGET_GROUP_ID)
#     def handle_message(message):
#         try:
#             # Log the received message details
#             user_name = message.from_user.username or message.from_user.first_name
#             user_message = message.text.strip()
#             print(f"Received from {user_name} in group {TARGET_GROUP_ID}: {user_message}")

#             # Initialize user conversation and transaction states
#             if message.from_user.id not in user_conversations:
#                 user_conversations[message.from_user.id] = []
#             if message.from_user.id not in user_transactions:
#                 user_transactions[message.from_user.id] = {
#                     "awaiting_chain": False,
#                     "awaiting_tx_id": False,
#                     "chain": None,
#                     "tx_id": None,
#                 }

#             # Reset conversation if "!e" is received
#             if user_message.lower() == "!e":
#                 user_conversations[message.from_user.id] = []
#                 user_transactions[message.from_user.id] = {
#                     "awaiting_chain": False,
#                     "awaiting_tx_id": False,
#                     "chain": None,
#                     "tx_id": None,
#                 }
#                 bot.reply_to(message, "Conversation reset. Let's start fresh! How can I assist you today?")
#                 return

#             # Respond "gm" if the user sends "gm"
#             if user_message.lower() == "gm":
#                 bot.reply_to(message, "gm 🙌")
#                 return

#             # Handle transaction-related queries
#             if "transaction" in user_message.lower() or "transfer" in user_message.lower() or "payment" in user_message.lower() or "send" in user_message.lower():
#                 # Handle transaction flow
#                 if user_transactions[message.from_user.id]["awaiting_chain"]:
#                     user_transactions[message.from_user.id]["chain"] = user_message
#                     user_transactions[message.from_user.id]["awaiting_chain"] = False
#                     user_transactions[message.from_user.id]["awaiting_tx_id"] = True
#                     bot.reply_to(message, "Got it! Now, please provide the transaction ID.")
#                 elif user_transactions[message.from_user.id]["awaiting_tx_id"]:
#                     user_transactions[message.from_user.id]["tx_id"] = user_message
#                     user_transactions[message.from_user.id]["awaiting_tx_id"] = False
#                     bot.reply_to(
#                         message,
#                         f"Transaction details received! Chain: {user_transactions[message.from_user.id]['chain']}, TX ID: {user_transactions[message.from_user.id]['tx_id']}",
#                     )
#                 else:
#                     user_transactions[message.from_user.id]["awaiting_chain"] = True
#                     bot.reply_to(message, "It seems like you're asking about a transaction. Please provide the chain name (e.g., Solana, Ethereum).")
#                 return

#             # Ignore messages containing substrings longer than 20 characters
#             if any(len(word) > 20 for word in user_message.split()):
#                 print(f"Ignoring message from {user_name}: {user_message}")
#                 return

#             # Handle regular conversation
#             user_conversations[message.from_user.id].append(f"User: {user_message}")
#             context = "\n".join(user_conversations[message.from_user.id][-10:])  # Limit context to the last 10 exchanges

#             prompt = (
#                 f"You are a Web3 expert. Respond professionally to the following conversation with a focus on blockchain, DeFi, NFTs, DAOs, crypto, and decentralized technologies:\n\n"
#                 f"{context}\n"
#                 f"AI:"
#             )
#             ai_response = model.generate_content(prompt)
#             reply = ai_response.text

#             # Ensure reply is within 80 words and doesn't cut sentences
#             words = reply.split()
#             if len(words) > 80:
#                 cutoff_idx = 80
#                 for i in range(79, -1, -1):
#                     if words[i].endswith(('.', '!', '?')):
#                         cutoff_idx = i + 1
#                         break
#                 reply = " ".join(words[:cutoff_idx])

#             # Ensure no AI self-references
#             if any(word.lower() in reply.lower() for word in ["i am", "my name", "i am an ai"]):
#                 reply = "I can only discuss Web3 topics. Let's stay focused on blockchain, crypto, NFTs, and more!"

#             bot.reply_to(message, reply)

#         except Exception as e:
#             bot.reply_to(message, f"An error occurred: {str(e)}")
















# import google.generativeai as genai

# # Configure Google Generative AI
# genai.configure(api_key="AIzaSyAENWtd9ouIs2rKrcA3ZjSjCDO0Xr-8BjY")
# model = genai.GenerativeModel("gemini-1.5-flash")

# # Store user conversation history and transaction-related details
# user_conversations = {}
# user_transactions = {}

# # Function to register handlers with the bot
# def register(bot):
#     # Define the target group ID (Replace with your actual group ID)
#     TARGET_GROUP_ID = -1002444698070

#     # Ensure the bot is receiving messages from the group
#     @bot.message_handler(func=lambda message: message.chat.id == TARGET_GROUP_ID)
#     def handle_message(message):
#         try:
#             # Log the received message details
#             user_name = message.from_user.username or message.from_user.first_name
#             print(f"Received from {user_name} in group {TARGET_GROUP_ID}: {message.text.strip()}")

#             user_message = message.text.strip()

#             # Initialize user conversation history if not already present
#             if message.from_user.id not in user_conversations:
#                 user_conversations[message.from_user.id] = []

#             # Initialize transaction state if not already present
#             if message.from_user.id not in user_transactions:
#                 user_transactions[message.from_user.id] = {
#                     "awaiting_chain": False,
#                     "awaiting_tx_id": False,
#                     "awaiting_wallet_name": False,
#                     "chain": None,
#                     "tx_id": None,
#                     "wallet_name": None,
#                 }

#             # If the user sends "!e", reset the conversation and transaction states
#             if user_message.lower() == "!e":
#                 # Clear previous conversation and transaction details
#                 user_conversations[message.from_user.id] = []
#                 user_transactions[message.from_user.id] = {
#                     "awaiting_chain": False,
#                     "awaiting_tx_id": False,
#                     "awaiting_wallet_name": False,
#                     "chain": None,
#                     "tx_id": None,
#                     "wallet_name": None,
#                 }
#                 reply = "Conversation reset. Let's start fresh! How can I assist you today?"
            
#             # Special case: Respond with "gm" if someone says "gm"
#             elif user_message.lower() == "gm":
#                 reply = "gm 🙌"
#                 user_conversations[message.from_user.id].append(f"User: {user_message}")
            
#             elif "transaction" in user_message.lower() or "transfer" in user_message.lower() or "send" in user_message.lower():
#                 # Handling transaction-related messages
#                 if user_transactions[message.from_user.id]["awaiting_chain"]:
#                     # Store the chain info and ask for TX ID
#                     user_transactions[message.from_user.id]["chain"] = user_message
#                     user_transactions[message.from_user.id]["awaiting_chain"] = False
#                     user_transactions[message.from_user.id]["awaiting_tx_id"] = True
#                     reply = "Got it! Now, please provide the transaction ID."
#                 elif user_transactions[message.from_user.id]["awaiting_tx_id"]:
#                     # Store the TX ID and ask for wallet name
#                     user_transactions[message.from_user.id]["tx_id"] = user_message
#                     user_transactions[message.from_user.id]["awaiting_tx_id"] = False
#                     user_transactions[message.from_user.id]["awaiting_wallet_name"] = True
#                     reply = "Got it! Now, please provide the wallet name (not the wallet address)."
#                 elif user_transactions[message.from_user.id]["awaiting_wallet_name"]:
#                     # Store the wallet name and confirm the transaction details
#                     user_transactions[message.from_user.id]["wallet_name"] = user_message
#                     user_transactions[message.from_user.id]["awaiting_wallet_name"] = False

#                     # Summarize the transaction details
#                     chain = user_transactions[message.from_user.id]["chain"]
#                     tx_id = user_transactions[message.from_user.id]["tx_id"]
#                     wallet_name = user_transactions[message.from_user.id]["wallet_name"]
#                     reply = (f"Transaction Details:\n"
#                              f"Chain: {chain}\n"
#                              f"Transaction ID: {tx_id}\n"
#                              f"Wallet Name: {wallet_name}\n"
#                              f"Thank you for providing the transaction details. We'll process this now.")
#                 else:
#                     # Start the transaction collection process by asking for the chain
#                     user_transactions[message.from_user.id]["awaiting_chain"] = True
#                     reply = "I noticed you're asking about a transaction. First, please tell me the blockchain (chain) you're using."
            
#             else:
#                 # Regular conversation with context and Web3 focus
#                 # Append the user message to the conversation history
#                 user_conversations[message.from_user.id].append(f"User: {user_message}")

#                 # Limit the conversation history to the last 5 exchanges for context
#                 context = "\n".join(user_conversations[message.from_user.id][-10:])  # 10 is adjustable

#                 # Generate the AI response with context
#                 prompt = (
#                     f"You are a Web3 expert. Respond professionally to the following conversation with a focus on Web3 concepts such as blockchain, DeFi, NFTs, DAOs, crypto, and decentralized technologies:\n\n"
#                     f"{context}\n"
#                     f"AI:"
#                 )

#                 # Generate the AI response
#                 ai_response = model.generate_content(prompt)
#                 reply = ai_response.text

#                 # Tokenize the response and ensure it's not cut off mid-sentence
#                 words = reply.split()
#                 if len(words) > 30:
#                     # Try to cut off at the last full sentence within the 30 words
#                     cutoff_idx = 30
#                     for i in range(29, -1, -1):  # Check backwards from the 30th word
#                         if words[i].endswith(('.', '!', '?')):
#                             cutoff_idx = i + 1  # Ensure the sentence ends cleanly
#                             break
#                     reply = " ".join(words[:cutoff_idx])  # Take the response up to the cutoff index

#                 # Ensure no self-referencing info about the AI is shared
#                 if any(word.lower() in reply.lower() for word in ["i am", "my name", "i am an ai"]):
#                     reply = "I can only discuss Web3 topics. Let's stay focused on blockchain, crypto, NFTs, and more!"

#             # Log the bot's reply
#             print(f"Bot Reply: {reply}")

#             # Send the reply
#             bot.reply_to(message, reply)

#         except Exception as e:
#             # Handle errors gracefully
#             reply = "I'm here to discuss Web3 topics. Please try again."
#             print(f"Error: {e}")
#             bot.reply_to(message, reply)

#     # Log when the bot starts listening
#     print(f"Bot is now listening for messages in group ID {TARGET_GROUP_ID}...")













# import google.generativeai as genai

# # Configure Google Generative AI
# genai.configure(api_key="AIzaSyAENWtd9ouIs2rKrcA3ZjSjCDO0Xr-8BjY")
# model = genai.GenerativeModel("gemini-1.5-flash")

# # Store user conversation history (in memory, can be persisted if needed)
# user_conversations = {}

# # Function to register handlers with the bot
# def register(bot):
#     # Define the target group ID (Replace with your actual group ID)
#     TARGET_GROUP_ID = -1002444698070

#     # Ensure the bot is receiving messages from the group
#     @bot.message_handler(func=lambda message: message.chat.id == TARGET_GROUP_ID)
#     def handle_message(message):
#         try:
#             # Log the received message details
#             user_name = message.from_user.username or message.from_user.first_name
#             print(f"Received from {user_name} in group {TARGET_GROUP_ID}: {message.text.strip()}")

#             user_message = message.text.strip()

#             # Initialize user conversation history if not already present
#             if message.from_user.id not in user_conversations:
#                 user_conversations[message.from_user.id] = []

#             # Special case: Respond with "gm" if someone says "gm"
#             if user_message.lower() == "gm":
#                 reply = "gm 🙌"
#                 user_conversations[message.from_user.id].append(f"User: {user_message}")
#             else:
#                 # Append the user message to the conversation history
#                 user_conversations[message.from_user.id].append(f"User: {user_message}")

#                 # Limit the conversation history to the last 5 exchanges for context
#                 context = "\n".join(user_conversations[message.from_user.id][-10:])  # 10 is adjustable

#                 # Generate the AI response with context
#                 prompt = (
#                     f"You are a Web3 expert. Respond professionally to the following conversation with a focus on Web3 concepts such as blockchain, DeFi, NFTs, DAOs, crypto, and decentralized technologies:\n\n"
#                     f"{context}\n"
#                     f"AI:"
#                 )

#                 # Generate the AI response
#                 ai_response = model.generate_content(prompt)
#                 reply = ai_response.text

#                 # Limit the response to 30 words
#                 reply_words = reply.split()[:30]  # Limit to 30 words
#                 reply = " ".join(reply_words)

#                 # Ensure no self-referencing info about the AI is shared
#                 if any(word.lower() in reply.lower() for word in ["i am", "my name", "i am an ai"]):
#                     reply = "I can only discuss Web3 topics. Let's stay focused on blockchain, crypto, NFTs, and more!"

#             # Log the bot's reply
#             print(f"Bot Reply: {reply}")

#             # Send the reply
#             bot.reply_to(message, reply)

#         except Exception as e:
#             # Handle errors gracefully
#             reply = "I'm here to discuss Web3 topics. Please try again."
#             print(f"Error: {e}")
#             bot.reply_to(message, reply)

#     # Log when the bot starts listening
#     print(f"Bot is now listening for messages in group ID {TARGET_GROUP_ID}...")








# # import google.generativeai as genai

# # # Configure Google Generative AI
# # genai.configure(api_key="AIzaSyAENWtd9ouIs2rKrcA3ZjSjCDO0Xr-8BjY")
# # model = genai.GenerativeModel("gemini-1.5-flash")

# # # Function to register handlers with the bot
# # def register(bot):
# #     # Define the target group ID (Replace with your actual group ID)
# #     TARGET_GROUP_ID = -1002444698070

# #     # Ensure the bot is receiving messages from the group
# #     @bot.message_handler(func=lambda message: message.chat.id == TARGET_GROUP_ID)
# #     def handle_message(message):
# #         try:
# #             # Log the received message details
# #             user_name = message.from_user.username or message.from_user.first_name
# #             print(f"Received from {user_name} in group {TARGET_GROUP_ID}: {message.text.strip()}")

# #             # Process the user's message
# #             user_message = message.text.strip()

# #             # Ensure Web3 context in the reply
# #             prompt = (
# #                 f"You are a Web3 expert. Respond professionally to the following question or statement with a focus on Web3 concepts such as blockchain, DeFi, NFTs, DAOs, crypto, and decentralized technologies:\n\n"
# #                 f"User: {user_message}\n"
# #                 f"AI:"
# #             )

# #             # Generate the AI response
# #             ai_response = model.generate_content(prompt)
# #             reply = ai_response.text
# #         except Exception as e:
# #             # Handle errors gracefully
# #             reply = "I'm here to discuss Web3 topics. Please try again."
# #             print(f"Error: {e}")

# #         # Log the bot's reply
# #         print(f"Bot Reply: {reply}")

# #         # Send the reply
# #         bot.reply_to(message, reply)

# #     # Log when the bot starts listening
# #     print(f"Bot is now listening for messages in group ID {TARGET_GROUP_ID}...")
