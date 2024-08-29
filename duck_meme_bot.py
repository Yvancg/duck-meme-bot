import os
import sys
import logging
import asyncio
import tempfile
from pathlib import Path
import requests
from telethon import TelegramClient
import tweepy

# Set up logging
logging.basicConfig(filename='bot.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Twitter API credentials
consumer_key = os.environ['TWITTER_API_KEY']
consumer_secret = os.environ['TWITTER_API_SECRET']
access_token = os.environ['TWITTER_ACCESS_TOKEN']
access_token_secret = os.environ['TWITTER_ACCESS_TOKEN_SECRET']

# Telegram API credentials
api_id = int(os.environ['TELEGRAM_API_ID'])
api_hash = os.environ['TELEGRAM_API_HASH']
telegram_channel = os.environ['TELEGRAM_CHANNEL']
bot_token = os.environ['TELEGRAM_BOT_TOKEN']

if not bot_token:
    logging.error("TELEGRAM_BOT_TOKEN environment variable is not set")
    sys.exit(1)

# Initialize Tweepy
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
twitter_api = tweepy.API(auth)

# Initialize Telegram Client
client = TelegramClient('anon', api_id, api_hash)

def download_image(image_url: str, timeout: int = 10) -> Path:
    try:
        response = requests.get(image_url, timeout=timeout)
        response.raise_for_status()
        with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as tmp_file:
            tmp_file.write(response.content)
            return Path(tmp_file.name)
    except requests.exceptions.RequestException as e:
        logging.error(f"Failed to download {image_url}: {e}")
        return None

async def process_tweet(tweet):
    if hasattr(tweet, 'extended_entities') and 'media' in tweet.extended_entities:
        for media in tweet.extended_entities['media']:
            if media['type'] == 'photo':
                image_url = media['media_url_https']
                file_path = download_image(image_url)
                if file_path:
                    try:
                        await client.send_file(telegram_channel, file_path, caption=tweet.full_text)
                        logging.info(f"Sent image to Telegram: {image_url}")
                    except Exception as e:
                        logging.error(f"Failed to send image to Telegram: {e}")
                    finally:
                        file_path.unlink()

async def main():
    try:
        await client.start(bot_token=bot_token)
        logging.info("Started Telegram client")
        
        tweets = tweepy.Cursor(twitter_api.search_tweets, q="#duckmemes -filter:retweets", lang="en", tweet_mode="extended").items(5)
        for tweet in tweets:
            await process_tweet(tweet)

        logging.info("Finished processing tweets")
    except Exception as e:
        logging.error(f"An error occurred during execution: {e}")
    finally:
        await client.disconnect()

if __name__ == '__main__':
    asyncio.run(main())
