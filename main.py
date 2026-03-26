import feedparser
import time
import requests
import re

TOKEN = "8754633021:AAHIvzlS7Xft0eYpWtXPOMjgyEYMTx4eBSc"
CHAT_ID = -5191302267
RSS_URL = "https://rsshub.rssforever.com/telegram/channel/Rhythmsssssss"

last_link = None

def clean_html(text):
    return re.sub('<.*?>', '', text)

def extract_images(text):
    return re.findall(r'<img.*?src="(.*?)"', text)

def extract_videos(text):
    return re.findall(r'href="(https://.*?\.mp4)"', text)

def send_message(text):
    requests.post(
        f"https://api.telegram.org/bot{TOKEN}/sendMessage",
        data={"chat_id": CHAT_ID, "text": text[:4000]}
    )

def send_photo(url, caption=""):
    requests.post(
        f"https://api.telegram.org/bot{TOKEN}/sendPhoto",
        data={"chat_id": CHAT_ID, "photo": url, "caption": caption[:1000]}
    )

def send_video(url, caption=""):
    requests.post(
        f"https://api.telegram.org/bot{TOKEN}/sendVideo",
        data={"chat_id": CHAT_ID, "video": url, "caption": caption[:1000]}
    )

def send_album(images, text):
    media = []

    for i, img in enumerate(images[:10]):  # Telegram лимит 10
        media.append({
            "type": "photo",
            "media": img,
            "caption": text if i == 0 else ""
        })

    requests.post(
        f"https://api.telegram.org/bot{TOKEN}/sendMediaGroup",
        json={"chat_id": CHAT_ID, "media": media}
    )

def send_post(entry):
    text = ""
    images = []
    videos = []

    if "summary" in entry:
        raw = entry.summary
        images = extract_images(raw)
        videos = extract_videos(raw)
        text = clean_html(raw)
    elif "title" in entry:
        text = entry.title

    # 🔥 1. альбом (если много фото)
    if len(images) > 1:
        send_album(images, text)

    # 🔥 2. одно фото
    elif len(images) == 1:
        send_photo(images[0], text)

    # 🔥 3. видео
    elif videos:
        send_video(videos[0], text)

    # 🔥 4. просто текст
    else:
        send_message(text)


while True:
    feed = feedparser.parse(RSS_URL)
    print("ENTRIES:", len(feed.entries))

    if feed.entries:
        entry = feed.entries[0]

        if entry.link != last_link:
            print("NEW POST:", entry.link)
            send_post(entry)
            last_link = entry.link

    time.sleep(20)
