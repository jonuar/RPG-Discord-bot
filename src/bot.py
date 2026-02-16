from discord.ext import commands
import asyncio
from fastapi import FastAPI
from db import connect_to_mongo
from config import DISCORD_TOKEN

app = FastAPI()
bot = commands.Bot(command_prefix="!")

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name} - {bot.user.id}')
    await connect_to_mongo()

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    await bot.process_commands(message)

@app.get("/")
async def root():
    return {"message": "Hello, this is the Discord bot API!"}

def run_bot():
    loop = asyncio.get_event_loop()
    loop.create_task(bot.start(DISCORD_TOKEN))
    loop.run_until_complete(app.run_async()) 

if __name__ == "__main__":
    run_bot()