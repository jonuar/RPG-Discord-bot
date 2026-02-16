# Discord FastAPI Bot

This project is a minimal boilerplate for a Discord bot built using `discord.py` and `FastAPI`, with MongoDB for data persistence.

## Project Structure

```
discord-fastapi-bot
├── src
│   ├── bot.py          # Entry point for the Discord bot
│   ├── api.py          # FastAPI application setup
│   ├── db.py           # MongoDB connection and CRUD operations
│   └── config.py       # Configuration settings
├── requirements.txt     # Project dependencies
└── README.md            # Project documentation
```

## Setup Instructions

1. **Clone the repository:**
   ```
   git clone <repository-url>
   cd discord-fastapi-bot
   ```

2. **Install dependencies:**
   ```
   pip install -r requirements.txt
   ```

3. **Configure your environment:**
   - Create a `.env` file or set environment variables for your Discord bot token and MongoDB connection string.
   - Example:
     ```
     DISCORD_TOKEN=your_discord_bot_token
     MONGODB_URI=your_mongodb_connection_string
     ```

4. **Run the bot:**
   ```
   python src/bot.py
   ```

## Usage

- The bot will connect to Discord and listen for events.
- You can define API endpoints in `api.py` to interact with the bot and perform actions based on incoming requests.

## Contributing

Feel free to submit issues or pull requests for improvements or additional features.