from matplotlib.pyplot import title
from werobot import WeRoBot
import datetime
import os
from WechatClient import WechatClient
from notify import send_message
from spider_box_office import spiderBoxOffice

from spider_movies import spiderMovies
from utils import getDayHowWeek
from wechat_acticle import generate_blockquote_html, generate_image_html, generate_indent_p_html, generate_info_html, generate_p_html, generate_title_html
from dotenv import load_dotenv
load_dotenv()
robot = WeRoBot()
robot.config["APP_ID"] = os.getenv('APP_ID')
robot.config["APP_SECRET"] = os.getenv('APP_SECRET')
# testID
# robot.config["APP_ID"] = "wxc5f26caf71891bb5"
# robot.config["APP_SECRET"] = "396bac1f1d8afb5c0c4588b3f7918fd1"


client = WechatClient(robot.config)


def upload_cover(path):
    '''
    上传封面图片
    '''
    data = client.upload_permanent_media(
        'image', open(path, 'rb'))
    return data['media_id']


def upload_article_image(path):
    '''
    上传文章图片
    '''
    data = client.upload_news_picture(open(path, 'rb'))
    return data['url']


def generate_html(movie):
    '''
    生成电影文章html
    '''
    title_text = generate_title_html(movie['title'])
    image_text = generate_image_html(movie['image'], movie['title'])
    summary_text = generate_indent_p_html(movie['summary'])
    hot_comment = movie['hot_comment']
    hot_comment_text = generate_blockquote_html(f'某瓣热评：{hot_comment}')
    info = movie['info'].split('\n')
    info = [generate_info_html(i) for i in info]
    info_text = ''.join(info)

    html = f'<div class="article">{title_text}{image_text}{info_text}{summary_text}{hot_comment_text}</div>'
    return html


def generate_box_office_text(data):
    '''
    生成一段box office 的文字描述
    '''
    first = data[-1]
    second = data[-2]
    text = f'''《{first['MovieName']}》领跑大盘，单月票房{first['boxoffice']}万，成绩算非常不错；《{second['MovieName']}》口碑可以也砍下{second['boxoffice']}万。'''
    return text


content = []
title = f'电影排行榜｜新片介绍｜{datetime.datetime.now().strftime("%Y年%m月")}'

movies = spiderMovies()
if len(movies) == 0:
    print(title + '没有新片')
    exit()
box_office = spiderBoxOffice()

box_office_image = upload_article_image(box_office['image'])
content.append(
    f'''{generate_p_html('先看上月票房排行榜')}{generate_image_html(box_office_image, '上月票房排行榜')}{generate_indent_p_html(generate_box_office_text(box_office['data']))}''')


media_id = upload_cover(movies[0]['image'])

for movie in movies:
    movie['image'] = upload_article_image(movie['image'])
    content.append(generate_html(movie))


article = {
    "title": title,
    "author": '爱买酱',
    "digest": '下个月有点东西',
    "content": '<div>{}<div>'.format(''.join(content)),
    "thumb_media_id": media_id,
}

try:
    data = client.create_draft([article])
    send_message(title, '爬取成功')
except:
    send_message(title, '爬取失败')
    exit()
