FROM python:3.10-slim

# Workdir in the container
WORKDIR /app

# Install dependencies
RUN pip install --no-cache-dir python-telegram-bot --upgrade

# Copy Bot code into the container
COPY main.py .

# Environment Variable for the Telegram-Bot-Token (set upon execution)
ENV TELEGRAM_BOT_TOKEN=""

# Start the bot
CMD ["python", "main.py"]
