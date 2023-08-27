import sys
import threading
import os
from time import sleep

root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(root_dir)

import src.utils.config as config
import src.entity.Device as dev
import src.utils.timedTasks as time_tasks

# 加载配置文件
config.load_config()


# 初始化设备信息
def load_dev():
    devices = []
    for device in config.devices:
        d = dev.Device(device['dev_name'],
                       device['dev_number'],
                       device['dev_username'],
                       device['dev_password'])
        time_tasks.start()
        devices.append(d)

    return devices


if __name__ == "__main__":
    devices = load_dev()
    threads = {}
    for device in devices:
        thread_name = f"t{device.DEV_NUMBER}"
        threads[thread_name] = threading.Thread(target=device.action)
        threads[thread_name].start()