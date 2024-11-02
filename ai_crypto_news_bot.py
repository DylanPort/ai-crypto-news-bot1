# File: ai_crypto_news_bot.py

import tweepy
import requests
from bs4 import BeautifulSoup
from PIL import Image
from io import BytesIO
import schedule
import time

# Twitter API credentials
API_KEY = "66EqHABre9o2PJzih8HjnPNI6"
API_SECRET_KEY = "QCIpbjSNzaqBKvlnqg43KdXtKoNYIFwUJdoPlzYCHtBRjXhNbL"
ACCESS_TOKEN = "1463262733634351119-L0DCeujtz0iuIiIKQivDF2PGkfaD0h"
ACCESS_TOKEN_SECRET = "PPqvRwcS2aIjbwJaeB0sbdYe6RNDUwObkxqZmfMdVmRBR"

# Authenticate with Twitter
auth = tweepy.OAuthHandler(API_KEY, API_SECRET_KEY)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
api = tweepy.API(auth)

# News sites to scrape
NEWS_SITES = [
    "https://www.coindesk.com/",
    "https://www.cryptonews.com/",
    "https://www.ainews.com/"
]

def get_latest_news():
    """Scrapes the latest news from specified sites."""
    news_posts = []
    for url in NEWS_SITES:
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            articles = soup.find_all('article', limit=1)  # Adjust to capture more or fewer articles
            
            for article in articles:
                title = article.find('h2').get_text() if article.find('h2') else "No Title"
                summary = article.find('p').get_text() if article.find('p') else "No Summary"
                img_tag = article.find('img')
                img_url = img_tag['src'] if img_tag else None
                
                news_posts.append({
                    "title": title,
                    "summary": summary,
                    "img_url": img_url
                })
    return news_posts

def post_to_twitter(news):
    """Formats and posts news articles to Twitter."""
    for article in news:
        tweet_text = f"{article['title']}\n\n{article['summary'][:100]}..."  # Limit summary to 100 chars
        
        if article['img_url']:
            # Download image and attach
            image_response = requests.get(article['img_url'])
            img = Image.open(BytesIO(image_response.content))
            img.save("temp_image.jpg")
            
            # Post tweet with image
            api.update_status_with_media(status=tweet_text, filename="temp_image.jpg")
        
        else:
            # Post tweet without image
            api.update_status(status=tweet_text)

def run_bot():
    """Runs the bot to fetch news and post to Twitter."""
    news = get_latest_news()
    if news:
        post_to_twitter(news)
    else:
        print("No news found to post.")

# Schedule the bot to run hourly
schedule.every().hour.do(run_bot)

print("Bot is running...")
while True:
    schedule.run_pending()
    time.sleep(1)
