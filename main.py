import feedparser
import time
import requests
import re

TOKEN = "ТВОЙ_ТОКЕН"
CHAT_ID = -5191302267

RSS_URLS = [
    "https://rsshub.rssforever.com/telegram/channel/Rhythmsssssss",
    "https://rsshub.moeyy.xyz/telegram/channel/Rhythmsssssss"
]

seen = set()

def clean_html(text):
    text = re.sub('<br ?/?>', '\n', text)
    text = re.sub('<.*?>', '', text)

    lines = text.split("\n")
    lines = [line.strip() for line in lines]

    return "\n".join([line for line in lines if line])

def extract_images(text):
    return re.findall(r'<img.*?src="(.*?)"', text)

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

def send_album(images, text):
    media = []

    for i, img in enumerate(images[:10]):
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

    if "summary" in entry:
        raw = entry.summary
        images = extract_images(raw)
        text = clean_html(raw)
    elif "title" in entry:
        text = entry.title

    if len(images) > 1:
        send_album(images, text)
    elif len(images) == 1:
        send_photo(images[0], text)
    else:
        send_message(text)

while True:
    for RSS_URL in RSS_URLS:
        feed = feedparser.parse(RSS_URL)

        if feed.entries:
            for entry in reversed(feed.entries[:7]):
                if entry.link not in seen:
                    print("NEW:", entry.link)
                    send_post(entry)
                    seen.add(entry.link)
                    time.sleep(2)

    time.sleep(8)
