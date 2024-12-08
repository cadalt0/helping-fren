import time
from telebot import types
from collections import defaultdict

# Initialize an empty bot variable, which will be populated by the register function
bot = None

# Fake leaderboard data
leaderboard = [
    {"name": "User1", "score": 10.5},
    {"name": "User2", "score": 9.75},
    {"name": "User3", "score": 8.8},
    {"name": "User4", "score": 7.9},
    {"name": "User5", "score": 6.5}
]

# Store user message count
user_message_count = defaultdict(int)

# Admins (replace with actual user IDs)
admins = [123456789, 987654321]  # Replace with real admin user IDs

# Register function to assign the bot instance
def register(bot_instance):
    global bot
    bot = bot_instance
    # Ensure bot is correctly initialized before registering handlers
    if bot:
        print("Bot successfully registered!")
    else:
        print("Failed to register bot. Bot instance is None.")

# Command to track message and update user score
def track_user_messages(message):
    user_id = message.from_user.id
    user_message_count[user_id] += 0.001  # Increment score by 0.001 for each message

# Leaderboard command
def show_leaderboard(message):
    # Fake leaderboard
    leaderboard_message = "Leaderboard:\n"
    for idx, user in enumerate(leaderboard, 1):
        leaderboard_message += f"{idx}. {user['name']} - {user['score']} points\n"
    
    # Create the button
    markup = types.InlineKeyboardMarkup()
    airdrop_button = types.InlineKeyboardButton("Airdrop", callback_data="airdrop")
    markup.add(airdrop_button)

    bot.send_message(message.chat.id, leaderboard_message, reply_markup=markup)

# Handle the airdrop button press (only for admins)
def handle_airdrop(call):
    if call.from_user.id in admins:
        bot.answer_callback_query(call.id, "Airdrop will be sent soon!")
        time.sleep(3)  # Simulate the delay for the airdrop
        bot.send_message(call.message.chat.id, "Airdrop sent!")
    else:
        bot.answer_callback_query(call.id, "You are not authorized to use this button.")

# Ensure the bot is registered and message handlers are assigned
if bot:
    bot.message_handler(func=lambda message: True)(track_user_messages)
    bot.message_handler(commands=['lw'])(show_leaderboard)
    bot.callback_query_handler(func=lambda call: call.data == "airdrop")(handle_airdrop)
else:
    print("Error: Bot is not registered. Ensure register(bot) is called before using handlers.")
