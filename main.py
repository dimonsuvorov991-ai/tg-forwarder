import feedparser
import time
import requests
import re

TOKEN = "8754633021:AAHIvzlS7Xft0eYpWtXPOMjgyEYMTx4eBSc"
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

def extract_audio(text):
    return re.findall(r'href="(https://.*?\.(mp3|ogg|wav))"', text)

def extract_video(text):
    return re.findall(r'href="(https://.*?\.(mp4))"', text)

def send_message(text):
    requests.post(
        f"https://api.telegram.org/bot{TOKEN}/sendMessage",
        data={"chat_id": CHAT_ID, "text": text[:4000]}
    )

def send_photo(url, caption=""):
    try:
        img = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}).content
        requests.post(
            f"https://api.telegram.org/bot{TOKEN}/sendPhoto",
            data={"chat_id": CHAT_ID, "caption": caption[:1000]},
            files={"photo": ("image.jpg", img)}
        )
    except Exception as e:
        print("PHOTO ERROR:", e)

def send_audio(url, caption=""):
    try:
        audio = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}).content
        requests.post(
            f"https://api.telegram.org/bot{TOKEN}/sendAudio",
            data={"chat_id": CHAT_ID, "caption": caption[:1000]},
            files={"audio": ("audio.mp3", audio)}
        )
    except Exception as e:
        print("AUDIO ERROR:", e)

def send_video(url, caption=""):
    try:
        video = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}).content
        requests.post(
            f"https://api.telegram.org/bot{TOKEN}/sendVideo",
            data={"chat_id": CHAT_ID, "caption": caption[:1000]},
            files={"video": ("video.mp4", video)}
        )
    except Exception as e:
        print("VIDEO ERROR:", e)

def send_post(entry):
    text = ""
    images = []
    audios = []
    videos = []

    if "summary" in entry:
        raw = entry.summary
        images = extract_images(raw)
        audios = extract_audio(raw)
        videos = extract_video(raw)
        text = clean_html(raw)
    elif "title" in entry:
        text = entry.title

    # 🎥 видео (приоритет)
    if videos:
        send_video(videos[0][0], text)

    # 🎧 аудио
    elif audios:
        send_audio(audios[0][0], text)

    # 📸 фото (альбом)
    elif len(images) > 1:
        for i, img in enumerate(images):
            send_photo(img, text if i == 0 else "")
            time.sleep(2)

    # 📸 одно фото
    elif len(images) == 1:
        send_photo(images[0], text)

    # 📝 текст
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
