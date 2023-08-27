import src.utils.config as config
import threading

# 加载配置文件
config.load_config()

import time


def task():
    while True:
        for message in config.send_messages:
            config.message = message['message']
            print(config.message)
            time.sleep(config.message_switch_time*60)


def start():
    thread = threading.Thread(target=task)
    thread.daemon = True
    thread.start()
