import sys
import threading
import os

root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(root_dir)

import src.utils.config as config
import src.entity.Device as dev
import src.utils.timedTasks as time_tasks

# ���������ļ�
config.load_config()


# ��ʼ���豸��Ϣ
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


def start():
    devices = load_dev()
    threads = {}

    for index, device in enumerate(devices):
        thread_name = f"t{index}"
        threads[thread_name] = threading.Thread(target=device.action)
        threads[thread_name].start()

