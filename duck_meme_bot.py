"""Module providing a function that fetches duck memes from X and posts them to Telegram."""

import os
from dotenv import load_dotenv
from pathlib import Path
import asyncio
import tempfile
import requests
from telethon import TelegramClient
from tweepy import OAuthHandler, API, Cursor

# Load environment variables from .env file
load_dotenv()

# Twitter API credentials from environment variables
consumer_key = os.getenv('TWITTER_API_KEY')
consumer_secret = os.getenv('TWITTER_API_SECRET')

# Debugging
print(f"Consumer Key: {consumer_key}")
print(f"Consumer Secret: {consumer_secret}")

access_token = os.getenv('TWITTER_ACCESS_TOKEN')
access_token_secret = os.getenv('TWITTER_ACCESS_TOKEN_SECRET')

# Telegram API credentials from environment variables
api_id = os.getenv('TELEGRAM_API_ID')
api_hash = os.getenv('TELEGRAM_API_HASH')
telegram_channel = os.getenv('TELEGRAM_CHANNEL')

# Initialize Tweepy
auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
twitter_api = API(auth)

# Initialize Telegram Client
client = TelegramClient('session_name', api_id, api_hash)

async def download_image(image_url: str, timeout: int = 10) -> Path:
    """Downloads an image from a URL and returns the local file path."""
    try:
        response = requests.get(image_url, timeout=timeout)
        response.raise_for_status()  # Raise an exception for HTTP errors
        with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as tmp_file:
            tmp_file.write(response.content)
            return Path(tmp_file.name)
    except requests.exceptions.RequestException as e:
        print(f"Failed to download {image_url}: {e}")
        return None

async def process_tweet(tweet):
    """Processes a single tweet, downloading images and sending them to Telegram."""
    if 'media' in tweet.entities:
        for image in tweet.entities['media']:
            image_url = image['media_url']
            file_path = await download_image(image_url)
            if file_path:
                await client.send_file(telegram_channel, file_path, caption=tweet.full_text)
                file_path.unlink()  # Remove the file after sending

async def main():
    """Main asynchronous function that automates the process."""
    await client.start()

    # Pylint: disable=not-an-iterable
    async for tweet in Cursor(twitter_api.search_tweets, q="#duckmemes -filter:retweets", lang="en", tweet_mode="extended").items(5):
        await process_tweet(tweet)

    print("Duck memes posted to Telegram channel.")

if __name__ == '__main__':
    asyncio.run(main())
