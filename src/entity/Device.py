import uiautomator2 as u2
from time import sleep
import src.utils.config as config

import src.utils.log as log

config.load_config()


class Device:
    DEV_NAME = ''
    # 设备编号
    DEV_NUMBER = 0
    DEV_USERNAME = ''
    DEV_PASSWORD = ''
    # ADB连接实例对象
    DEV = None
    # ADB 连接状态
    DEV_ADB_STATUS = False
    # 是否存在新消息
    NEW_SESSION = None
    # 终止信号
    TERMINATION_SIGNAL = False
    # 剩余消息数
    REMAINING_MESSAGES = config.message_max

    def __init__(self, dev_name, dev_number, dev_username, dev_password):
        self.DEV_NAME = dev_name
        self.DEV_NUMBER = dev_number
        self.DEV_USERNAME = dev_username
        self.DEV_PASSWORD = dev_password
        self.connect()

    # 建立连接
    def connect(self):
        try:
            self.DEV = u2.connect(self.DEV_NAME)
            # 切换成FastInputIME输入法
            self.DEV.set_fastinput_ime(True)
            self.DEV.app_start(config.package_name, config.home_page)
            self.DEV_ADB_STATUS = True
            log.info(self, f'建立连接成功!!! ')
        except Exception as e:
            log.error(self, f'adb连接异常!!! {str(e)}')
            self.DEV_ADB_STATUS = False

    # 操作单元
    def action(self):
        # 检测是否发送终止信号
        if self.TERMINATION_SIGNAL:
            log.info(self, '停止运行成功')
            return
        self.activity_check()
        self.slide()
        try:
            if self.concern():
                if self.to_user_home():
                    self.to_send_page()
                    self.click_msg_box(config.message)
                    self.send()
                    self.back()
                    self.back()
                    self.back()
            elif not self.exist(config.comment_area):
                return self.action()
            return self.action()
        except Exception as e:
            print(e)
            log.error(self, f'操作异常，尝试重启中{e}')
            self.action()

    # 活动检测
    def activity_check(self):

        if self.DEV.current_app()['package'] == config.package_name:
            if self.DEV.current_app()['activity'] in [config.home_page, f'{config.package_name}{config.home_page}']:
                return True
            else:
                self.reboot()
        else:
            self.reboot()

    # 判断是否存在某个界面元素
    def exist(self, name: str):
        return self.DEV(resourceId=name).exists

    # 重启app
    def reboot(self):
        self.DEV.app_stop(config.package_name)
        self.DEV.app_start(config.package_name, config.home_page)
        # 等待加载
        sleep(10)
        self.activity_check()

    # 滑动下个视频
    def slide(self):
        self.DEV.shell('input swipe 350 1000 350 300 200')
        sleep(config.sleep_time)

    # 关注
    def concern(self):
        if self.exist(config.concern):
            self.DEV(resourceId=config.concern).click()
            sleep(config.sleep_time)
            return True
        else:
            # log.warning(self, '找不到关注按钮!!!')
            return False

    # 进入用户主页
    def to_user_home(self):
        if self.exist(config.user_home):
            self.DEV(resourceId=config.user_home).click()
            sleep(config.sleep_time)
            return True
        else:
            # log.warning(self, '找不到进入用户主页的头像')
            return False

    # 进入私信
    def to_send_page(self):
        if self.exist(config.private_messages):
            self.DEV(resourceId=config.private_messages).click()
            sleep(config.sleep_time)
            return True
        else:
            return False

    # 点击 发送消息框输入
    def click_msg_box(self, msg: str):
        if self.exist(config.private_message_box):
            self.DEV(resourceId=config.private_message_box).click()
            sleep(config.sleep_time)
            self.DEV.send_keys(msg)  # 输入文字
            sleep(config.sleep_time)
            return True
        else:
            return False

    # 点击发送
    def send(self):
        if self.exist(config.send_button):
            if not self.REMAINING_MESSAGES == 0:
                self.REMAINING_MESSAGES = self.REMAINING_MESSAGES - 1
                left = self.DEV(resourceId=config.send_button).info.get("bounds").get('left')
                top = self.DEV(resourceId=config.send_button).info.get("bounds").get('top')
                self.DEV.click(left + 20, top + 20)
                sleep(config.sleep_time)
                return True
            else:
                log.info(self, '当前账户发送消息已达上限')
                self.TERMINATION_SIGNAL = True
        else:
            return False

    # 返回操作
    def back(self):
        self.DEV.press('back')
        sleep(0.5)
