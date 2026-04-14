from dotenv import load_dotenv
import discord
import os

load_dotenv()
token = os.getenv("TOKEN")
if not token:
    raise SystemExit("Set TOKEN in .env (Discord bot token).")

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)


@client.event
async def on_ready():
    print(f"We have logged in as {client.user}")


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith("$hello"):
        await message.channel.send("Hello!")


if __name__ == "__main__":
    client.run(token)
