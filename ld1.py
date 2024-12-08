import time
from telebot import TeleBot, types
from collections import defaultdict

# Initialize the bot with your token
bot_token = '8170472328:AAEWjgQBQ04jwwlbmwU-JH7wDz0qXunACww'  # Replace with your actual bot token
bot = TeleBot(bot_token)

# Fake leaderboard data
leaderboard = [
    {"name": "User1", "score": 10.5},
    {"name": "User2", "score": 9.75},
    {"name": "User3", "score": 8.8},
    {"name": "User4", "score": 7.9},
    {"name": "User5", "score": 6.5}
]

# Store user message count
user_message_count = defaultdict(float)

# Admins (replace with actual user IDs)
admins = [1053006285, 987654321]  # Replace with real admin user IDs

# Command to show leaderboard
@bot.message_handler(commands=['leaderboard'])
def show_leaderboard(message):
    leaderboard_text = "Leaderboard:\n"
    for idx, entry in enumerate(leaderboard, 1):
        leaderboard_text += f"{idx}. {entry['name']}: {entry['score']} points\n"
    
    # Create a button
    markup = types.InlineKeyboardMarkup()
    airdrop_button = types.InlineKeyboardButton("Airdrop", callback_data="airdrop")
    markup.add(airdrop_button)
    
    bot.send_message(message.chat.id, leaderboard_text, reply_markup=markup)

# Handle button click
@bot.callback_query_handler(func=lambda call: call.data == "airdrop")
def handle_airdrop(call):
    if call.from_user.id in admins:
        bot.answer_callback_query(call.id, "Airdrop will be sent shortly!")
        time.sleep(3)  # Simulate delay for the airdrop
        bot.send_message(call.message.chat.id, "Airdrop sent!")
    else:
        bot.answer_callback_query(call.id, "You are not authorized to perform this action.")

# Echo received messages (basic functionality)
@bot.message_handler(func=lambda message: True)
def echo_all(message):
    user_id = message.from_user.id
    user_message_count[user_id] += 0.001
    bot.reply_to(message, f"Message received: {message.text}\n"
                          f"Your current message count: {user_message_count[user_id]:.3f}")

# Run the bot
if __name__ == "__main__":
    print("Bot is running...")
    bot.polling(none_stop=True)
