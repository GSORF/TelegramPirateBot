# Pirate Spam Guard Bot

A Telegram bot that protects your group from spam and inactive newcomers with a fun pirate twist! New members must introduce themselves within 60 minutes or be kicked (“keelhauled”). Built with Python and the [python-telegram-bot](https://github.com/python-telegram-bot/python-telegram-bot) library, and easy to deploy with Docker.

---

## Features

- **Pirate-style greeting** for each new chat member  
- **60-minute grace period** to send a personal message  
- **Automatic removal** (ban) of users who remain silent  
- **In-memory tracking** of pending users  
- `/start` command for testing in private chat  
- Lightweight, stateless design — no external database

---

## Prerequisites

- Python 3.10+
- A Telegram bot token (from [BotFather](https://t.me/BotFather))
- Docker & Docker Compose (optional, for containerized deployment)

---

## Getting Started

### 1. Clone this repository

```bash
git clone https://github.com/yourusername/pirate-spam-guard.git
cd pirate-spam-guard
```

### 2. Set your bot token

Create a .env file in the project root:

```bash
echo "TELEGRAM_BOT_TOKEN=your_bot_token_here" > .env
```

    Note: Never commit your bot token to version control.

### 3. Install dependencies

```bash
pip install --upgrade python-telegram-bot
```

## Usage
Run Locally

```bash
export TELEGRAM_BOT_TOKEN="$(grep TELEGRAM_BOT_TOKEN .env | cut -d '=' -f2)"
python main.py
```

## Bot Commands

    /start — Verify the bot is running (private chat only).

    Automatic greeting & enforcement on new chat members.

### Docker

Build the Docker image:

```bash
docker build -t pirate-spam-guard-bot:latest .
```

Run the container (replace YOUR_BOT_TOKEN_HERE):

```bash
docker run -d \
  --name pirate-spam-guard-bot \
  -e TELEGRAM_BOT_TOKEN=YOUR_BOT_TOKEN_HERE \
  --restart unless-stopped \
  pirate-spam-guard-bot:latest
```

## Docker Compose

A docker-compose.yml is provided for convenience:

```bash
version: '3.8'
services:
  spamguard-bot:
    build:
      context: .
      dockerfile: Dockerfile
    image: pirate-spam-guard-bot:latest
    restart: unless-stopped
    environment:
      TELEGRAM_BOT_TOKEN: "YOUR_BOT_TOKEN_HIER"
```

## Start with:

```bash
docker-compose up -d
```

## Project Structure

```bash
├── Dockerfile
├── docker-compose.yml
├── main.py
└── README.md
```

    main.py — Bot logic and handlers

    Dockerfile — Container setup

    docker-compose.yml — Orchestration

## Contributing

    Fork the repo

    Create your feature branch (git checkout -b feature/YourFeature)

    Commit your changes (git commit -am "Add some feature")

    Push to the branch (git push origin feature/YourFeature)

    Open a Pull Request

Please adhere to the existing coding style and include tests where appropriate.
License

This project is licensed under the MIT License. See the LICENSE file for details.














