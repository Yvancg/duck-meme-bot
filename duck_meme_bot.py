import os
import requests
from telethon import TelegramClient
from tweepy import OAuthHandler, API, Cursor

# Twitter API credentials
consumer_key = 'YOUR_TWITTER_API_KEY'
consumer_secret = 'YOUR_TWITTER_API_SECRET'
access_token = 'YOUR_TWITTER_ACCESS_TOKEN'
access_token_secret = 'YOUR_TWITTER_ACCESS_TOKEN_SECRET'

# Telegram API credentials
api_id = 'YOUR_TELEGRAM_API_ID'
api_hash = 'YOUR_TELEGRAM_API_HASH'
telegram_channel = 'YOUR_TELEGRAM_CHANNEL_USERNAME'

# Initialize Tweepy
auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
twitter_api = API(auth)

# Initialize Telegram Client
client = TelegramClient('session_name', api_id, api_hash)

async def main():
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