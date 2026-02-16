import os

class Config:
    DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
    MONGODB_URL = os.getenv("MONGODB_URL")
    PORT = int(os.getenv("PORT", 8000))