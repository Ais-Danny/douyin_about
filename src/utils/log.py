import logging
from colorama import Fore, Style
logging.basicConfig(filename="out.log", filemode="a",encoding="utf-8",
                    format="%(asctime)s %(name)s:%(levelname)s:%(message)s",
                    datefmt="%d-%M-%Y %H:%M:%S", level=logging.INFO)


def error(dev, msg: str):
    logging.error(f':{dev.DEV_NUMBER} {msg}')
    print(Fore.RED + f'ERROR:' + Style.RESET_ALL + f'设备编号:{dev.DEV_NUMBER} {msg}')


def warning(dev, msg: str):
    logging.warning(f'{dev.DEV_NUMBER} {msg}')
    print(Fore.YELLOW + 'WARNING:' + Style.RESET_ALL + f'设备编号:{dev.DEV_NUMBER} {msg}')


def info(dev, msg: str):
    logging.info(f'{dev.DEV_NUMBER} {msg}')
    print(Fore.GREEN + 'INFO:' + Style.RESET_ALL + f'设备编号:{dev.DEV_NUMBER} {msg}')
