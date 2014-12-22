import json
import wget
import yaml
from os import mkdir
from urllib import request


USER_NAME = (str(input("Paste user name: ").strip()))
# Load config
try:
    with open("config.yaml") as f:
        config = yaml.load(f.read())
except FileNotFoundError:
    raise "Error in frontend: couldn't find frontend.yaml config."
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
            url = '%s\n' % img['images']['standard_resolution']['url']
            print(url)
            wget.download(url, USER_NAME)
    next_page_url = feed.get('pagination')
    if next_page_url:
        download_feed(next_page_url['next_url'])

def get_user_id(user_name):
    user_id = None
    user_url = "https://api.instagram.com/v1/users/search?" + \
        "q={USER_NAME}&client_id={CLIENT_ID}"
    user_url = user_url.format(USER_NAME=user_name, CLIENT_ID=CLIENT_ID)
    resp = request.urlopen(user_url)
    feed = resp.read()
    feed = json.loads(feed.decode("utf-8"))
    data = feed.get('data')
    if data:
        for user in data:
            if user['username'] == user_name:
                user_id = user['id']
                break
    return user_id

def main():
    # Get user_id by user_name
    USER_ID = get_user_id(USER_NAME)
    # Create dir
    try:
        mkdir(USER_NAME)
    except Exception as exp:
        print(exp)
    # Download user feed
    if (USER_ID):
        recent_url = "https://api.instagram.com/v1/users/{USER_ID}/" + \
            "media/recent/?client_id={YOUR_CLIENT_ID}"
        url = recent_url.format(USER_ID=USER_ID, YOUR_CLIENT_ID=CLIENT_ID)
        download_feed(url)
    else:
        raise "There is no any user with this username."


if __name__ == '__main__':
    main()
    