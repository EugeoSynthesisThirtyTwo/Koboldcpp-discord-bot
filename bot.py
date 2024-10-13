import discord
import requests
import json

# Discord Bot Token (replace with your actual bot token)
DISCORD_TOKEN = 'YOUR_DISCORD_BOT_TOKEN'
KOBOLDCPP_API_URL = 'http://127.0.0.1:5000/api/generate'

# Define the bot
intents = discord.Intents.default()
intents.messages = True

client = discord.Client(intents=intents)

# Function to generate a response using KoboldCpp
def generate_response(prompt):
    data = {
        'prompt': prompt,
        'max_length': 150,  # Control how long the response is
        'temperature': 0.7,  # Adjust for randomness in responses
        'top_k': 50,
        'top_p': 0.9
    }
    
    try:
        response = requests.post(KOBOLDCPP_API_URL, json=data)
        response_json = response.json()
        if 'text' in response_json:
            return response_json['text']
        else:
            return "Error: No response generated."
    except Exception as e:
        return f"Error communicating with KoboldCpp: {e}"

# Event when the bot has connected
@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

# Event when the bot receives a message
@client.event
async def on_message(message):
    # Ignore the bot's own messages
    if message.author == client.user:
        return
    
    # Simple trigger to respond when bot is mentioned or a command like !ai is used
    if message.content.startswith('!ai'):
        prompt = message.content[len('!ai '):]
        
        # Generate a response using KoboldCpp
        response = generate_response(prompt)
        
        # Send the response back to Discord
        await message.channel.send(response)

# Run the bot
client.run(DISCORD_TOKEN)
