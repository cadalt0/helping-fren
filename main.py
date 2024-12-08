import telebot
import importlib.util
import os

# Replace 'YOUR_API_KEY' with your bot's API key
API_KEY = 'token'

# Initialize the bot
bot = telebot.TeleBot(API_KEY)

# Function to load and execute a module (extension)
def load_extension(filename):
    try:
        spec = importlib.util.spec_from_file_location(filename, filename)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        
        # Check if the module has a register function and call it
        if hasattr(module, "register"):
            module.register(bot)  # Register the module with the bot
            print(f"Successfully loaded and registered: {filename}")
        else:
            # Still load and execute the module even if it doesn't have a register function
            print(f"Module {filename} does not have a 'register' function, but it was still loaded.")
        
        return module
    except Exception as e:
        print(f"Failed to load {filename}: {e}")

# Automatically load all Python files in the current directory as extensions
def load_all_extensions():
    for file in os.listdir():
        if file.endswith(".py") and file != "bot_main.py":  # Skip main file
            load_extension(file)

if __name__ == "__main__":
    print("Loading extensions...")
    load_all_extensions()  # Load all extensions
    print("Bot is running...")
    try:
        bot.infinity_polling()  # Start the bot
    except Exception as e:
        print(f"An error occurred: {e}")




# import telebot
# import importlib.util
# import os

# # Replace 'YOUR_API_KEY' with your bot's API key
# API_KEY = '8170472328:AAEWjgQBQ04jwwlbmwU-JH7wDz0qXunACww'

# # Initialize the bot
# bot = telebot.TeleBot(API_KEY)

# # Function to load and execute a module (extension)
# def load_extension(filename):
#     try:
#         spec = importlib.util.spec_from_file_location(filename, filename)
#         module = importlib.util.module_from_spec(spec)
#         spec.loader.exec_module(module)
#         # Check if the module has a register function and call it
#         if hasattr(module, "register"):
#             module.register(bot)  # Register the module with the bot
#             print(f"Successfully loaded: {filename}")
#         else:
#             print(f"Module {filename} does not have a 'register' function.")
#         return module
#     except Exception as e:
#         print(f"Failed to load {filename}: {e}")

# # Automatically load all Python files in the current directory as extensions
# def load_all_extensions():
#     for file in os.listdir():
#         if file.endswith(".py") and file != "bot_main.py":  # Skip main file
#             load_extension(file)

# if __name__ == "__main__":
#     print("Loading extensions...")
#     load_all_extensions()  # Load all extensions
#     print("Bot is running...")
#     try:
#         bot.infinity_polling()  # Start the bot
#     except Exception as e:
#         print(f"An error occurred: {e}")
