
# Duck Meme Bot

## Overview

Duck Meme Bot is an automated bot that sources duck memes from X.com (formerly Twitter) using the `#duckmemes` hashtag and posts them to a specified Telegram channel. The bot is scheduled to run hourly using GitHub Actions, ensuring that your Telegram channel is continuously updated with fresh content.

## Features

- **Automated Meme Sourcing**: Fetches the latest duck memes from X.com.
- **Telegram Integration**: Posts the memes directly to a Telegram channel.
- **Cron Job Automation**: Runs automatically every hour using GitHub Actions.

## Setup Instructions

### Prerequisites

- Python 3.x
- A GitHub account
- A Telegram account with access to the Telegram API
- A Twitter Developer account with API credentials

### Local Development Setup

1. **Clone the Repository:**

   ```bash
   git clone https://github.com/yvancg/duck-meme-bot.git
   cd duck-meme-bot
   ```

2. **Create and Activate a Virtual Environment:**

   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install the Required Libraries:**

   ```bash
   pip install -r requirements.txt
   ```

4. **Configure API Credentials:**

   Update the placeholder values in `duck_meme_bot.py` with your actual API credentials for Twitter and Telegram. You can also set these as environment variables for better security.

### Running the Script Locally

To test the bot locally, activate your virtual environment and run the script:

```bash
python duck_meme_bot.py
```

This will fetch the latest duck memes and post them to your configured Telegram channel.

### GitHub Actions Setup

The bot is configured to run automatically every hour using GitHub Actions. The workflow is defined in `.github/workflows/cron-job.yml`.

1. **Push the Repository to GitHub:**

   If not done already, push your local repository to GitHub:

   ```bash
   git add .
   git commit -m "Initial commit"
   git push -u origin main
   ```

2. **Set Up Secrets on GitHub:**

   Add your Twitter and Telegram API credentials as secrets in your GitHub repository settings:

   - `TWITTER_API_KEY`
   - `TWITTER_API_SECRET`
   - `TWITTER_ACCESS_TOKEN`
   - `TWITTER_ACCESS_TOKEN_SECRET`
   - `TELEGRAM_API_ID`
   - `TELEGRAM_API_HASH`

3. **Check the GitHub Actions:**

   Navigate to the "Actions" tab in your GitHub repository to monitor the workflow and ensure that the bot is running as expected.

## Customization

- **Hashtag:** You can change the hashtag used to source memes by editing the `q="#duckmemes -filter:retweets"` line in `duck_meme_bot.py`.
- **Schedule:** Adjust the cron schedule in `.github/workflows/cron-job.yml` to change how often the bot runs.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request or open an issue to discuss any improvements.

## License

This project is open-source and available under the [MIT License](LICENSE).

```

### Summary of the README Sections:

- **Overview:** A brief description of what the project does.
- **Features:** Highlights the key functionalities.
- **Setup Instructions:** Step-by-step guide to setting up the project locally and using GitHub Actions.
- **Running the Script Locally:** Instructions on how to test the bot.
- **GitHub Actions Setup:** Details on setting up the cron job using GitHub Actions.
- **Customization:** Tips on how to modify the bot’s behavior.
- **Contributing:** Encouragement for community contributions.
- **License:** Information about the project's license.
