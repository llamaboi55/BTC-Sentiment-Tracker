import os
import time
import threading
from collections import deque
from datetime import datetime

import praw
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt

# — Configuration — 
COIN         = "BTC"
SUBREDDITS   = ["CryptoCurrency", "Bitcoin", "ethereum"]
INTERVAL_SEC = 5    # seconds between scrapes
PLOT_UPDATE  = 5    # seconds between redraws
HISTORY_LEN  = (5 * 24 * 60 * 60) // INTERVAL_SEC  # 5 days buffer

# Load Reddit credentials from env
CLIENT_ID     = os.getenv("REDDIT_CLIENT_ID")
CLIENT_SECRET = os.getenv("REDDIT_CLIENT_SECRET")
USER_AGENT    = os.getenv("REDDIT_USER_AGENT")
if not all([CLIENT_ID, CLIENT_SECRET, USER_AGENT]):
    raise RuntimeError("Set REDDIT_CLIENT_ID, REDDIT_CLIENT_SECRET & REDDIT_USER_AGENT")

# Rolling buffers
timestamps       = deque(maxlen=HISTORY_LEN)
mention_counts   = deque(maxlen=HISTORY_LEN)
sentiment_scores = deque(maxlen=HISTORY_LEN)

# Initialize APIs
reddit   = praw.Reddit(
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    user_agent=USER_AGENT
)
analyzer = SentimentIntensityAnalyzer()

def fetch_and_analyze():
    now = datetime.utcnow()
    count = 0
    score = 0.0

    for sub in SUBREDDITS:
        for comment in reddit.subreddit(sub).comments(limit=100):
            txt = comment.body.upper()
            if f"#{COIN}" in txt or f" {COIN} " in txt:
                count += 1
                score += analyzer.polarity_scores(txt)["compound"]

    # map [-1,1] → [0,100]
    avg = (score / count) if count else 0
    sentiment = int(round((avg + 1) * 50))

    timestamps.append(now)
    mention_counts.append(count)
    sentiment_scores.append(sentiment)

    print(f"{now:%Y-%m-%d %H:%M:%S}  mentions={count:<3}  sentiment={sentiment}")

def poller():
    while True:
        fetch_and_analyze()
        time.sleep(INTERVAL_SEC)

def live_chart():
    plt.ion()
    fig, ax1 = plt.subplots()
    ax2 = ax1.twinx()
    last_draw = datetime.utcnow()

    while True:
        now = datetime.utcnow()
        if (now - last_draw).total_seconds() >= PLOT_UPDATE and timestamps:
            ax1.clear(); ax2.clear()
            ax1.plot(timestamps, mention_counts,   '-o', label="Mentions")
            ax2.plot(timestamps, sentiment_scores, '-o', label="Sentiment", linestyle="--")
            ax1.set_ylabel("Mentions")
            ax2.set_ylabel("Sentiment (1–100)")
            ax1.set_xlabel("Time (UTC)")
            plt.title(f"{COIN} Mentions & Sentiment")
            fig.autofmt_xdate()
            ax1.legend(loc="upper left"); ax2.legend(loc="upper right")
            last_draw = now
        plt.pause(0.1)

if __name__ == "__main__":
    threading.Thread(target=poller, daemon=True).start()
    live_chart()
