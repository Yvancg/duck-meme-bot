"""Module providing a function that fetches duck memes from Twitter and posts them to Telegram."""

import os
from pathlib import Path
import asyncio
import tempfile
import requests
from telethon import TelegramClient
import tweepy

# Twitter API credentials from environment variables
consumer_key = os.environ['TWITTER_API_KEY']
consumer_secret = os.environ['TWITTER_API_SECRET']
access_token = os.environ['TWITTER_ACCESS_TOKEN']
access_token_secret = os.environ['TWITTER_ACCESS_TOKEN_SECRET']

# Telegram API credentials from environment variables
api_id = int(os.environ['TELEGRAM_API_ID'])
api_hash = os.environ['TELEGRAM_API_HASH']
telegram_channel = os.environ['TELEGRAM_CHANNEL']
bot_token = os.environ['TELEGRAM_BOT_TOKEN']

if not bot_token:
    raise ValueError("TELEGRAM_BOT_TOKEN environment variable is not set")

# Initialize Tweepy
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
twitter_api = tweepy.API(auth)

# Initialize Telegram Client
client = TelegramClient('session_name', api_id, api_hash)

def download_image(image_url: str, timeout: int = 10) -> Path:
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
    if hasattr(tweet, 'extended_entities') and 'media' in tweet.extended_entities:
        for media in tweet.extended_entities['media']:
            if media['type'] == 'photo':
                image_url = media['media_url_https']
                file_path = download_image(image_url)
                if file_path:
                    await client.send_file(telegram_channel, file_path, caption=tweet.full_text)
                    file_path.unlink()  # Remove the file after sending

async def run():
    """Runs the Telegram client and processes tweets."""
    async with client:
        await client.start(bot_token=bot_token)
        
        tweets = tweepy.Cursor(twitter_api.search_tweets, q="#duckmemes -filter:retweets", lang="en", tweet_mode="extended").items(5)
        for tweet in tweets:
            await process_tweet(tweet)

        print("Duck memes posted to Telegram channel.")

def main():
    """Main entry point for running the bot."""
    try:
        asyncio.run(run())
    except (KeyboardInterrupt, SystemExit):
        print("Exiting...")

if __name__ == '__main__':
    main()