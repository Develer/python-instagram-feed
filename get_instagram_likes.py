import json
import sys
import wget
import yaml
from os import mkdir
from urllib import request


# Load config
try:
    with open("myconfig.yaml") as f:
        config = yaml.load(f.read())
except FileNotFoundError:
    raise "couldn't find config.yaml config."
except Exception as e:
    raise "Error: %s" % e
CLIENT_ID = config['CLIENT_ID']
CLIENT_SECRET = config['CLIENT_SECRET']
REDIRECT_URI = config['REDIRECT_URI']


def download_feed(url):
    resp = request.urlopen(url)
    feed = resp.read()
    feed = json.loads(feed.decode("utf-8"))
    data = feed.get('data')
    if data:
        for img in feed['data']:
            url = '%s' % img['images']['standard_resolution']['url']
            try:
                wget.download(url, "likes")
                sys.stdout.flush()
            except Exception as e:
                print("Error: %s" % e)
    next_page_url = feed.get('pagination')
    if next_page_url:
        download_feed(next_page_url['next_url'])


if __name__ == '__main__':
    # Create dir
    try:
        mkdir("likes")
    except Exception as exp:
        print(exp)

    # Get token
    token_url = "https://instagram.com/oauth/authorize/" + \
        "?client_id={CLIENT_ID}&redirect_uri={REDIRECT_URI}&response_type=token"
    token_url = token_url.format(CLIENT_ID=CLIENT_ID, REDIRECT_URI=REDIRECT_URI)
    resp = request.urlopen(token_url)
    print("Use this url form token generating: {TOKEN_URL}".format(
        TOKEN_URL=resp.url))

    TOKEN = (str(input("Paste generated token: ").strip()))

    likes_url = "https://api.instagram.com/v1/users/self/media/liked" + \
        "?access_token={TOKEN}"
    likes_url = likes_url.format(TOKEN=TOKEN)
    download_feed(likes_url)
