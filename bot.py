import discord
import requests
import os
from src.config import settings
from src.character import load_character_card

# Define the bot
intents = discord.Intents.default()
intents.messages = True
client = discord.Client(intents=intents)

bot_name = "bot"
character = None

# Function to generate a response using KoboldCpp
def generate_response(prompt) -> str:
    data = {
        'prompt': prompt,
        'max_length': 150,  # Control how long the response is
        'temperature': 0.7,  # Adjust for randomness in responses
        'top_k': 50,
        'top_p': 0.9
    }

    try:
        response = requests.post(settings.koboldcpp_api_url, json=data)
        response_json = response.json()
        if 'text' in response_json:
            return response_json['text']
        else:
            return "Error: No response generated."
    except Exception as e:
        return f"Error communicating with KoboldCpp: {e}"

# Function to list and load character files
def list_character_files():
    characters_path = "characters"
    character_files = [f for f in os.listdir(characters_path) if f.endswith('.json')]
    return character_files

async def show_character_selection(channel):
    character_files = list_character_files()
    if not character_files:
        await channel.send("No character files found.")
        return None
    
    options = "\n".join([f"{i+1}. {file}" for i, file in enumerate(character_files)])
    await channel.send(f"Available characters:\n{options}\nPlease select a character by entering the corresponding number.")
    return character_files

# Event when the bot has connected
@client.event
async def on_ready():
    global bot_name
    bot_name = client.user.name  # Retrieve the bot's name
    print(f'Logged in as {bot_name} (ID: {client.user.id})')

# Event when the bot receives a message
@client.event
async def on_message(message):
    global character

    # Ignore the bot's own messages
    if message.author == client.user:
        return

    # List available characters when the user types "!select"
    if message.content.startswith('!select'):
        character_files = await show_character_selection(message.channel)

        if not character_files:
            return  # No files to select

        def check(m):
            return m.author == message.author and m.content.isdigit()

        try:
            selection_message = await client.wait_for('message', check=check, timeout=30.0)
            selection_index = int(selection_message.content) - 1
            if 0 <= selection_index < len(character_files):
                selected_file = character_files[selection_index]
                character = load_character_card(f'characters/{selected_file}')
                await message.channel.send(f"Character {selected_file} loaded successfully.")
            else:
                await message.channel.send("Invalid selection. Please try again.")
        except Exception as e:
            await message.channel.send("Character selection timed out or an error occurred.")
    
    # Simple trigger to respond when bot is mentioned or a command like !ai is used
    if message.content.startswith('!ai'):
        prompt = message.content[len('!ai '):]
        
        if character:
            # Generate a response using KoboldCpp with the selected character
            response = generate_response(f"Character: {character}\nPrompt: {prompt}")
        else:
            response = "No character selected. Please use !select to choose a character."

        # Send the response back to Discord
        await message.channel.send(response)

# Run the bot using the token from the .env file
client.run(settings.discord_token)
