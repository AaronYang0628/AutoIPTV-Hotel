import re


def extract_base(url):
    match = re.match(r"^(https?://[^/]+)", url)
    if match:
        return match.group(1)
    return ""


def process_url(base_url, url):
    if ',' in url:
        return None
    if 'http' in url:
        return url
    else:
        return f"{extract_base(base_url)}{url}"


def replace_cctv(name):
    name = name.replace("cctv", "CCTV")
    name = name.replace("中央", "CCTV")
    name = name.replace("央视", "CCTV")
    name = name.replace("高清", "")
    name = name.replace("超高", "")
    name = name.replace("HD", "")
    name = name.replace("标清", "")
    name = name.replace("频道", "")
    name = name.replace("-", "")
    name = name.replace(" ", "")
    name = name.replace("PLUS", "+")
    name = name.replace("＋", "+")
    name = name.replace("(", "")
    name = name.replace(")", "")
    name = re.sub(r"CCTV(\d+)台", r"CCTV\1", name)
    name = re.sub(r"[\u4e00-\u9fff]", "", name)
    return name


if __name__ == '__main__':
    print(replace_cctv("CCTV10科教"))
