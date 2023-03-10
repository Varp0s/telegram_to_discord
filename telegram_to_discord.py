import requests
import discord
from datetime import datetime
import asyncio

# Telegram API key
TELEGRAM_TOKEN = "change"

# Discord bot token
DISCORD_TOKEN = "change"

# Telegram group ID
GROUP_ID = "change"

# Discord channel ID
CHANNEL_ID = "change"

#time between each check
POLL_INTERVAL = 10

# Keep track of the last message ID
last_message_offset = 0

pwi = "Powered by"
varp = "Varp0s"
pw = "@everyone"


def get_group_messages(GROUP_ID):
    """
    Fetch the messages from Telegram group
    """
    global last_message_offset
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/getUpdates?chat_id={GROUP_ID}&offset={last_message_offset}&limit=100"
        res = requests.get(url)
        data = res.json()
        messages = data['result']
        if messages:
            last_message_offset = messages[-1]['update_id'] + 1
            
        return messages
    except Exception as e:
        print(f'Error: {e}')
        return None

# Initialize the Discord client
intents = discord.Intents().all()
client = discord.Client(intents=intents)

# Send the messages to Discord
@client.event
async def on_ready():
    channel = client.get_channel(int(CHANNEL_ID))
    while True:
        messages = get_group_messages(GROUP_ID)
        if messages:
            for message in messages:
                try:
                    if 'text' in message["message"]:
                        text = message["message"]["text"]
                    else:
                        text = 'Not a Text message'
                    try:
                        username = message["message"]["from"]["username"]
                    except KeyError as e:
                        username = 'Unknown'
                    try:
                        timestamp = datetime.fromtimestamp(message["message"]["date"]).strftime('%Y-%m-%d %H:%M:%S')
                    except KeyError as e:
                        timestamp = 'Unknown'
                    if len(text) > 2000:
                        chunks = [text[i:i + 1900] for i in range(0, len(text), 2000)]
                        
                        for chunk in chunks:
                            await channel.send(f"{username} ({timestamp}): {chunk}")
                            await channel.send(f"{pwi} {varp} {pw}")
                    else:
                        await channel.send(f"{username} ({timestamp}): {text}")
                        await channel.send(f"{pwi} {varp} {pw}")
                except KeyError as e:
                    print(f'Error: {e}')
                    pass
        await asyncio.sleep(POLL_INTERVAL)

client.run(DISCORD_TOKEN)




