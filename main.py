import feedparser
import time
import requests

TOKEN = "8754633021:AAHIvzlS7Xft0eYpWtXPOMjgyEYMTx4eBSc"
CHAT_ID = -5191302267
RSS_URL = "https://rsshub.rssforever.com/telegram/channel/Rhythmsssssss"

posted = set()

def send_message(text):
    requests.post(
        f"https://api.telegram.org/bot{TOKEN}/sendMessage",
        data={"chat_id": CHAT_ID, "text": text}
    )

def send_photo(url, caption=""):
    requests.post(
        f"https://api.telegram.org/bot{TOKEN}/sendPhoto",
        data={"chat_id": CHAT_ID, "photo": url, "caption": caption}
    )

def send_video(url, caption=""):
    requests.post(
        f"https://api.telegram.org/bot{TOKEN}/sendVideo",
        data={"chat_id": CHAT_ID, "video": url, "caption": caption}
    )

def send_post(entry):
    text = entry.title if entry.title else ""
    media_urls = []

    if "media_content" in entry:
        for media in entry.media_content:
            media_urls.append(media["url"])

    if len(media_urls) > 1:
        for i, media in enumerate(media_urls):
            if media.endswith(".mp4"):
                send_video(media, text if i == 0 else "")
            else:
                send_photo(media, text if i == 0 else "")
            time.sleep(2)

    elif len(media_urls) == 1:
        media = media_urls[0]
        if media.endswith(".mp4"):
            send_video(media, text)
        else:
            send_photo(media, text)

    else:
        send_message(text)

while True:
    feed = feedparser.parse(RSS_URL)
    print("ENTRIES:", len(feed.entries))

    for entry in reversed(feed.entries):
        if entry.link not in posted:
            send_post(entry)
            posted.add(entry.link)
            time.sleep(5)

    time.sleep(30)
