# BTC-Sentiment-Tracker
# Crypto Sentiment Tracker

A lightweight Python script that tracks mentions of a single cryptocurrency (BTC) in live Reddit comments across your favorite subreddits, computes a simple 0–100 sentiment index using VADER, and plots both counts and sentiment in real time.

---

## Features

- Scrapes the latest comments from selected subreddits via the official [PRAW](https://praw.readthedocs.io/) library  
- Counts how many times `#BTC` (or ` BTC `) appears in recent comments  
- Runs [VADER](https://github.com/cjhutto/vaderSentiment) sentiment analysis on those comments  
- Maintains a rolling buffer of the last ±5 days at 5-second resolution  
- Displays an auto-scaling, dual-axis Matplotlib chart that updates live  

---

## Setup

1. **Clone this repository**  
   ```bash
   git clone https://github.com/yourusername/crypto-sentiment-tracker.git
   cd crypto-sentiment-tracker
Install dependencies

bash
Copy code
pip install praw vaderSentiment matplotlib
Register a Reddit “script” app

Visit https://www.reddit.com/prefs/apps

Click “create another app…”

Give it a name (e.g. CryptoSentimentTracker), select Script, and set Redirect URI to http://localhost

Copy the Client ID (the 14-character string under your app’s name) and Secret

Configure credentials
Create a file named .env in the project root (or export these in your shell):

bash
Copy code
REDDIT_CLIENT_ID=your_client_id_here
REDDIT_CLIENT_SECRET=your_client_secret_here
REDDIT_USER_AGENT="crypto-sentiment-tracker by /u/your_reddit_username"
Then, install python-dotenv if you like, or export them directly:

bash
Copy code
export REDDIT_CLIENT_ID=...
export REDDIT_CLIENT_SECRET=...
export REDDIT_USER_AGENT="crypto-sentiment-tracker by /u/you"
Run the tracker

bash
Copy code
python sentiment_tracker_reddit.py
