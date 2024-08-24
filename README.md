
```markdown
# Duck Meme Bot

Duck Meme Bot is an automated Python script that fetches duck-related memes from X.com (formerly Twitter) and posts them to a specified Telegram channel. The bot runs periodically using GitHub Actions, making it a fully automated solution for your meme-sharing needs.

## Features

- Fetches the latest duck memes from X.com using the `#duckmemes` hashtag.
- Automatically posts the memes to a specified Telegram channel.
- Runs periodically every hour using a cron job configured in GitHub Actions.

## Requirements

- Python 3.x
- Virtual environment (`venv`)
- Tweepy (`tweepy`) - For interacting with the Twitter API
- Telethon (`telethon`) - For interacting with the Telegram API
- Requests (`requests`) - For handling HTTP requests

## Setup

### 1. Clone the Repository

```bash
git clone https://github.com/yvancg/duck-meme-bot.git
cd duck-meme-bot
```

### 2. Create and Activate a Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```

### 3. Install the Required Dependencies

```bash
pip install -r requirements.txt
```

### 4. Set Up API Keys and Environment Variables

You'll need to set up the following environment variables to store your API keys and other credentials:

- **Twitter API:**
  - `TWITTER_API_KEY`
  - `TWITTER_API_SECRET`
  - `TWITTER_ACCESS_TOKEN`
  - `TWITTER_ACCESS_TOKEN_SECRET`

- **Telegram API:**
  - `TELEGRAM_API_ID`
  - `TELEGRAM_API_HASH`
  - `TELEGRAM_CHANNEL`

You can either export these variables in your shell or create a `.env` file in your project directory.

### 5. Running the Script Locally

To test the bot locally, ensure your virtual environment is active, then run:

```bash
python duck_meme_bot.py
```

### 6. Automating with GitHub Actions

This project includes a GitHub Actions workflow that automatically runs the bot every hour.

- The workflow file is located at `.github/workflows/cron-job.yml`.
- The cron job is scheduled using the following cron expression: `0 * * * *`, meaning it runs at the start of every hour.

To enable the GitHub Actions workflow:

1. Push your changes to the `main` branch.
2. GitHub Actions will automatically trigger the workflow according to the schedule.

### 7. Monitor the Workflow

You can monitor the workflow runs in the "Actions" tab of your GitHub repository.

## Contributing

Contributions are welcome! If you have suggestions for improvements, please feel free to fork the repository and submit a pull request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
```

### Additional Instructions

1. **Update the Repository URL**: Replace the `git clone` URL with the correct URL for your repository.
2. **Environment Variables**: The README assumes you're familiar with setting environment variables. If not, you may want to add instructions or examples on how to do this.

### Optional Sections
You can also add optional sections, such as:
- **Screenshots**: Include screenshots of the bot in action.
- **Troubleshooting**: Provide common issues and solutions.
- **Acknowledgments**: Give credit to any libraries or resources used.
