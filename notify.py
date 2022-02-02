import os
import requests
from dotenv import load_dotenv
load_dotenv()

SEND_KEY = os.getenv('SEND_KEY')


def send_message(title, message=''):
    url = f'https://sctapi.ftqq.com/{SEND_KEY}.send?title={title}&desp={message}'
    requests.get(url)
