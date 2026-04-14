from dotenv import load_dotenv
from openai import OpenAI
import discord
import os

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY") or os.getenv("OPENAI_KEY")
DISCORD_TOKEN = os.getenv("TOKEN")

if not api_key:
    raise SystemExit("Set OPENAI_API_KEY or OPENAI_KEY in .env (needed for $question).")
if not DISCORD_TOKEN:
    raise SystemExit("Set TOKEN in .env (Discord bot token).")

openai_client = OpenAI(api_key=api_key)

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)


def call_openai(question: str) -> str:
    r = openai_client.chat.completions.create(
        model=os.getenv("MODEL") or "gpt-4o",
        messages=[
            {"role": "user", "content": f"Respond like a AI scientist to the following question: {question}"},
        ],
    )
    return (r.choices[0].message.content or "").strip()


@client.event
async def on_ready():
    print(f"Logged in as {client.user}")


@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if message.content.startswith("$hello"):
        await message.channel.send("Hello!")
    elif message.content.startswith("$question"):
        q = message.content.split("$question", 1)[1]
        try:
            text = call_openai(q)
        except Exception as e:
            text = f"Sorry, I couldn't answer that: {e}"
        await message.channel.send(text[:2000])

    if message.content.startswith('$question'):
        print(f"Message: {message.content}")                
        message_content = message.content.split("$question")[1]
        print(f"Question: {message_content}")    
        response = call_openai(message_content)   
        print(f"Assistant: {response}")    
        print("---")
        await message.channel.send(response)

client.run(DISCORD_TOKEN)
