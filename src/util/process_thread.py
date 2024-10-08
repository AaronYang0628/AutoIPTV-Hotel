import os

import eventlet
import requests
import time
from queue import Queue

eventlet.monkey_patch()

error_channels = []


# 定义工作线程函数
def worker(task_queue: Queue, valid_channels: list):
    while True:
        # 从队列中获取一个任务
        channel_name, channel_url = task_queue.get()

        try:
            channel_url_t = channel_url.rstrip(channel_url.split('/')[-1])  # m3u8链接前缀
            lines = requests.get(channel_url, timeout=1).text.strip().split('\n')  # 获取m3u8文件内容
            ts_lists = [line.split('/')[-1] for line in lines if line.startswith('#') == False]  # 获取m3u8文件下视频流后缀
            ts_lists_0 = ts_lists[0].rstrip(ts_lists[0].split('.ts')[-1])  # m3u8链接前缀
            ts_url = channel_url_t + ts_lists[0]  # 拼接单个视频片段下载链接

            # 多获取的视频数据进行5秒钟限制
            with eventlet.Timeout(5, False):
                start_time = time.time()
                content = requests.get(ts_url, timeout=1).content
                end_time = time.time()
                response_time = (end_time - start_time) * 1

            if content:
                with open(ts_lists_0, 'ab') as f:
                    f.write(content)  # 写入文件
                file_size = len(content)
                download_speed = file_size / response_time / 1024

                # 删除下载的文件
                os.remove(ts_lists_0)
                valid_channels.append((channel_name, channel_url, download_speed))
                # numberx = (len(results) + len(error_channels)) / len(channels) * 100
                print(
                    # f"可用频道：{len(results)} 个 , 不可用频道：{len(error_channels)} 个 , 总频道：{len(channels)} 个 ,总进度：{numberx:.2f} %。")
                    f"可用频道：{len(valid_channels)} 个 , 不可用频道：{len(error_channels)} 个 ")
        except:
            error_channel = channel_name, channel_url
            error_channels.append(error_channel)
            # numberx = (len(results) + len(error_channels)) / len(channels) * 100
            print(
                # f"可用频道：{len(results)} 个 , 不可用频道：{len(error_channels)} 个 , 总频道：{len(channels)} 个 ,总进度：{numberx:.2f} %。")
                f"可用频道：{len(valid_channels)} 个 , 不可用频道：{len(error_channels)} 个 ")
        # 标记任务完成
        task_queue.task_done()
