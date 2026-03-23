 if len(media_urls) > 1:
        for i, media in enumerate(media_urls):
            try:
                if media.endswith(".mp4"):
                    bot.send_video(chat_id=CHAT_ID, video=media, caption=text if i == 0 else "")
                else:
                    bot.send_photo(chat_id=CHAT_ID, photo=media, caption=text if i == 0 else "")
                time.sleep(2)
            except Exception as e:
                print(e)

    # если одно медиа
    elif len(media_urls) == 1:
        media = media_urls[0]
        try:
            if media.endswith(".mp4"):
                bot.send_video(chat_id=CHAT_ID, video=media, caption=text)
            else:
                bot.send_photo(chat_id=CHAT_ID, photo=media, caption=text)
        except:
            bot.send_message(chat_id=CHAT_ID, text=text)

    # если нет медиа
    else:
        bot.send_message(chat_id=CHAT_ID, text=text)


while True:
    feed = feedparser.parse(RSS_URL)

    for entry in reversed(feed.entries):
        if entry.link not in posted:
            try:
                send_post(entry)
                posted.add(entry.link)
                time.sleep(5)
            except Exception as e:
                print(e)

    time.sleep(30)

