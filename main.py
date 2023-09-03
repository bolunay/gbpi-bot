import praw
import time
import requests
from lxml import html
import random

reddit = praw.Reddit(
    client_id="",
    client_secret="",
    username="",
    password="",
    user_agent="",
) # credentials

subreddit_name = "kgbtr"

reply_text_template = """İşte sana güzel bir porno

[İNDİR]({download_link})

[İZLE]({watch_now_link})

^(ben u/bolunayy tarafından yapılmış bir botum.)
"""

def get_download_link():
    url = "https://www.saveporn.net/last-downloads/"
    response = requests.get(url)
    tree = html.fromstring(response.text)
    xpath = f"/html/body/main/section[4]/div/div[{random.randint(1, 16)}]/a"
    element = tree.xpath(xpath)
    href_value = element[0].get("href")
    download_link = "https://www.saveporn.net" + href_value
    return download_link

def get_watch_now_link(download_link):
    wn_response = requests.get(download_link)
    tree = html.fromstring(wn_response.text)
    wn_xpath = f"/html/body/main/section[3]/div/div[1]/a"
    element = tree.xpath(wn_xpath)
    href_value = element[0].get("href")
    return href_value

def reply_with_link(comment):
    download_link = get_download_link()
    watch_now_link = get_watch_now_link(download_link)
    reply_text = reply_text_template.format(download_link=download_link, watch_now_link=watch_now_link)

    comment.reply(reply_text)

while True:
    try:
        subreddit = reddit.subreddit(subreddit_name)
        for comment in subreddit.stream.comments(skip_existing=True):
            if comment.author.name != "GuzelBirPornoIndir1":
                if f"u/{reddit.user.me()}" in comment.body:
                    reply_with_link(comment)
                elif "güzel bir porno indir" in comment.body.lower():
                    reply_with_link(comment)
                elif "güzel bir porno indir" == comment.author_flair_text.lower():
                    reply_with_link(comment)
    except Exception as e:
        print(f"bir hata oldu: {e}")
        time.sleep(10)