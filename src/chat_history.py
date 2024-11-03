import discord

async def fetch_channel_history(bot: discord.Client, channel_id: int, num_messages: int) -> list[tuple[str, str]]:
    """Fetches the last `num_messages` from the specified channel.

    Args:
        bot (discord.Client): The Discord bot client.
        channel_id (int): The ID of the Discord channel.
        num_messages (int): The number of messages to retrieve.

    Returns:
        List[Tuple[str, str]]: A list of tuples containing (username, message content).
    """
    channel = bot.get_channel(channel_id)
    if not channel:
        print("Channel not found!")
        return []

    messages_data = []

    async for message in channel.history(limit=num_messages):
        messages_data.append((message.author.display_name, message.content))

    messages_data.reverse()

    return messages_data