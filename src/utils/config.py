import yaml

package_name = ''
home_page = ''
concern = ''
private_messages = ''
private_message_box = ''
send_button = ''
user_home = ''
comment_area = ''

sleep_time = 0
message_max = 0
message_switch_time = 0
send_messages = ''
message = ''
devices = None


def load_config():
    global devices
    global package_name
    global home_page
    global concern
    global private_messages
    global private_message_box
    global send_button
    global user_home
    global comment_area

    global sleep_time
    global message_max
    global message_switch_time
    global send_messages
    global message
    with open('config.yaml', 'r',encoding='utf-8') as f:
        data = yaml.safe_load(f)
        package_name = data.get('package_name', '')
        home_page = data.get('home_page', '')
        concern = data.get('concern', '')
        private_messages = data.get('private_messages', '')
        private_message_box = data.get('private_message_box', '')
        send_button = data.get('send_button', '')
        user_home = data.get('user_home', '')
        comment_area = data.get('comment_area', '')
        devices = data.get('devices', [])

        sleep_time = data.get('sleep_time', 0)
        message_max = data.get('message_max', 0)
        message_switch_time = data.get('message_switch_time', 0)
        send_messages = data.get('send_messages', '')
