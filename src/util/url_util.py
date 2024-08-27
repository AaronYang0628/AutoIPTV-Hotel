import re

import requests


def is_url_accessible(url):
    try:
        response = requests.get(url, timeout=0.5)
        if response.status_code == 200:
            return url
    except requests.exceptions.RequestException:
        pass
    return None


def generate_urls(url:str):
    urls = []
    for i in range(1, 256):
        new_url = re.sub(r"(\.\d+)(:\d+)", fr".{i}\2", url)
        urls.append(f"{new_url}/iptv/live/1000.json?key=txiptv")
    return urls


def extract_base(url):
    match = re.match(r"^(https?://[^/]+)", url)
    if match:
        return match.group(1)
    return ""

if __name__ == '__main__':
    url = 'http://60.255.137.106:9901/iptv/live/1000.json?key=txiptv'

    print(extract_base(url))
