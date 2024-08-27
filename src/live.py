import time
import concurrent.futures
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import requests
import re
import threading
from queue import Queue
import eventlet

from iptv.string_util import replace_cctv, process_url
from util.process_thread import worker
from util.url_util import generate_urls, is_url_accessible
from util.m3u_file_generator import M3UFileGenerator
from util.sample_file_generator import SampleFileGenerator

eventlet.monkey_patch()

fofa_links = [
    "https://fofa.info/result?qbase64=ImlwdHYvbGl2ZS96aF9jbi5qcyIgJiYgY291bnRyeT0iQ04iICYmIHJlZ2lvbj0iU2ljaHVhbiI%3D",
    # 四川
    "https://fofa.info/result?qbase64=ImlwdHYvbGl2ZS96aF9jbi5qcyIgJiYgY291bnRyeT0iQ04iICYmIHJlZ2lvbj0i5LqR5Y2XIg%3D%3D",
    # 云南
    "https://fofa.info/result?qbase64=ImlwdHYvbGl2ZS96aF9jbi5qcyIgJiYgY291bnRyeT0iQ04iICYmIHJlZ2lvbj0iQ2hvbmdxaW5nIg%3D%3D",
    # 重庆
    "https://fofa.info/result?qbase64=ImlwdHYvbGl2ZS96aF9jbi5qcyIgJiYgY291bnRyeT0iQ04iICYmIHJlZ2lvbj0iR3VpemhvdSI%3D",
    # 贵州
    "https://fofa.info/result?qbase64=ImlwdHYvbGl2ZS96aF9jbi5qcyIgJiYgY291bnRyeT0iQ04iICYmIHJlZ2lvbj0iU2hhbnhpIg%3D%3D",
    # 山西
    "https://fofa.info/result?qbase64=ImlwdHYvbGl2ZS96aF9jbi5qcyIgJiYgY291bnRyeT0iQ04iICYmIHJlZ2lvbj0iR3Vhbmd4aSBaaHVhbmd6dSI%3D",
    # 广西
    # "https://fofa.info/result?qbase64=ImlwdHYvbGl2ZS96aF9jbi5qcyIgJiYgY291bnRyeT0iQ04iICYmIHJlZ2lvbj0iWmhlamlhbmci", #浙江
    # "https://fofa.info/result?qbase64=ImlwdHYvbGl2ZS96aF9jbi5qcyIgJiYgY291bnRyeT0iQ04iICYmIHJlZ2lvbj0iU2hhbmdoYWki", #上海
    # "https://fofa.info/result?qbase64=ImlwdHYvbGl2ZS96aF9jbi5qcyIgJiYgY291bnRyeT0iQ04iICYmIHJlZ2lvbj0iQmVpamluZyI%3D", #北京
]

results = []

for link in fofa_links:
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')

    driver = webdriver.Chrome(options=chrome_options)
    driver.get(link)
    time.sleep(10)
    page_content = driver.page_source

    driver.quit()

    print(f"fofa link -> {link}")
    candidate_urls = re.findall(r"http://\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}:\d+", page_content)
    print(f"url candidates -> {candidate_urls}")
    base_urls = []
    for url_item in set(candidate_urls):
        base_urls.append(re.sub(r"(\.\d+)(:\d+)", r".1\2", url_item))

    base_urls = set(base_urls)
    print(f"base urls -> {base_urls}")

    accessible_urls = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=100) as executor:
        futures = []
        for base_url in base_urls:
            for modified_url in generate_urls(base_url.strip()):
                futures.append(executor.submit(is_url_accessible, modified_url))

        for future in concurrent.futures.as_completed(futures):
            result = future.result()
            if result:
                accessible_urls.append(result)

    print(f"accessible urls -> {accessible_urls}")

    for request_url in accessible_urls:
        try:
            json_data = requests.get(request_url, timeout=0.5).json()
            try:
                for item in json_data['data']:
                    if isinstance(item, dict):
                        if item.get('name') and item.get('url'):
                            results.append((replace_cctv(item.get('name')), process_url(request_url, item.get('url'))))
            except:
                continue
        except:
            continue


# 线程安全的队列，用于存储下载任务
task_queue = Queue()
for channel in results:
    task_queue.put(channel)

# 线程安全的列表，用于存储结果
content_lines = []

# 创建多个工作线程
for _ in range(10):
    t = threading.Thread(target=worker, daemon=True, args=(task_queue, content_lines))
    t.start()

# 等待所有任务完成
task_queue.join()


content_lines.sort(key=lambda x: (x[0], float(x[2])))

M3UFileGenerator(candidate_count=8).export(results, "lives.m3u")
SampleFileGenerator(candidate_count=2).export(results, "cctv.m3u")
