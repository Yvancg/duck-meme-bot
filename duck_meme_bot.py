""" Module providing a function that fetches duck memes from X and posts them to Telegram."""

import os
import requests
from telethon import TelegramClient
from tweepy import OAuthHandler, API, Cursor
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Twitter API credentials from environment variables
consumer_key = os.getenv('TWITTER_API_KEY')
consumer_secret = os.getenv('TWITTER_API_SECRET')
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


async def main():
    """ Main asynchronous function that automates the process """
    # Ensure you're authorized
    await client.start()

    # Search for recent tweets with #duckmemes hashtag
    for tweet in Cursor(twitter_api.search_tweets, q="#duckmemes -filter:retweets", lang="en", tweet_mode="extended").items(5):
        if 'media' in tweet.entities:
            for image in tweet.entities['media']:
                image_url = image['media_url']
                image_data = requests.get(image_url).content
                filename = 'duck_meme.jpg'
                with open(filename, 'wb') as handler:
                    handler.write(image_data)
              
                # Send the image to the Telegram channel
                await client.send_file(telegram_channel, filename, caption=tweet.full_text)

                # Remove the downloaded image after sending
                os.remove(filename)

    print("Duck memes posted to Telegram channel.")

with client:
    client.loop.run_until_complete(main())
