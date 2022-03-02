from webptools import dwebp
import requests
from bs4 import BeautifulSoup
import os
import json
import time

from utils import isInNextWeek, isNextMonth
s = requests.Session()
# get douban coming movie list
headers = {
    'Connection': 'keep-alive',
    'Cache-Control': 'max-age=0',
    'sec-ch-ua': '"Chromium";v="92", " Not A;Brand";v="99", "Google Chrome";v="92"',
    'sec-ch-ua-mobile': '?0',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-User': '?1',
    'Sec-Fetch-Dest': 'document',
    'Referer': 'https://movie.douban.com/coming?sequence=desc',
    'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7,zh-TW;q=0.6',
    'Cookie': 'bid=-XxHhy3Yi4A; ll="118099"; __gads=ID=b05a206f81e187ba-2266ac1ea2cb00d0:T=1631670820:RT=1631670820:S=ALNI_MZQdF2h9pxmZIXp2KuNv5UiKVNEYw; __gpi=00000000-0000-0000-0000-000000000000&ZG91YmFuLmNvbQ==&Lw==; __utmc=30149280; gr_user_id=70469d94-f059-47de-b1ec-07ac11082bab; viewed="30247885_25926153_1083139_1880126_5408893_1058010_1179303_1818527_30143702"; __utmc=223695111; _vwo_uuid_v2=DCC2FA09466B4BB0228B6B87FCFE4C321|3d165cfad6442500a396189d4d41c351; ck=_ep6; __utmv=30149280.21974; _ga=GA1.2.1241558271.1632808366; _gid=GA1.2.1186091195.1641992913; ap_v=0,6.0; _pk_ref.100001.4cf6=%5B%22%22%2C%22%22%2C1642000963%2C%22https%3A%2F%2Fwww.douban.com%2F%22%5D; _pk_ses.100001.4cf6=*; __utma=30149280.1241558271.1632808366.1641992699.1642000963.12; __utmb=30149280.0.10.1642000963; __utmz=30149280.1642000963.12.6.utmcsr=douban.com|utmccn=(referral)|utmcmd=referral|utmcct=/; __utma=223695111.304327830.1639125866.1641992699.1642000963.6; __utmb=223695111.0.10.1642000963; __utmz=223695111.1642000963.6.5.utmcsr=douban.com|utmccn=(referral)|utmcmd=referral|utmcct=/; _pk_id.100001.4cf6=cced5894b0bde180.1639125865.6.1642001214.1641993775.'
}

url = 'https://movie.douban.com/coming'


r = s.get(url, headers=headers)
soup = BeautifulSoup(r.text, 'html.parser')

tbody = soup.find('tbody')

trs = tbody.find_all('tr')


class Movie:
    def __init__(self, title, url, sort_id):
        self.title = title
        self.url = url
        self.sort_id = sort_id
        self.soup = self.getSoup()
        self.info = self.getInfo()
        self.image_webp = self.downloadPhoto()
        self.image = self.toJpeg()
        self.summary = self.getSummary()
        self.hot_comment = self.getHotComment()

    def getHtml(self):
        r = s.get(self.url, headers=headers)
        return r.text

    def getSoup(self):
        return BeautifulSoup(self.getHtml(), 'html.parser')

    def getInfo(self):
        return self.soup.find('div', id='info').text.strip()

    def getSummary(self):
        try:
            return self.soup.find('div', id='link-report').text.strip()
        except:
            return '暂无简介'

    def getHotComment(self):
        return self.soup.find('div', id='hot-comments').find('p').text.strip()

    def getPhotoPath(self):
        return self.soup.find('div', id='mainpic').find('img')['src']

    def downloadPhoto(self):
        r = s.get(self.getPhotoPath())
        path = os.path.join('photos-webp', self.title + '.webp')
        if not os.path.exists(os.path.dirname(path)):
            os.mkdir(os.path.dirname(path))
        with open(path, 'wb') as f:
            f.write(r.content)
        return path

    def toJpeg(self):
        input_image = self.image_webp
        output_image = os.path.join('photos', self.title + '.jpg')
        if not os.path.exists(os.path.dirname(output_image)):
            os.mkdir(os.path.dirname(output_image))
        dwebp(input_image=input_image, output_image=output_image,
              option='-o', logging='-v')
        return output_image

    def toDict(self):
        return {
            'title': self.title,
            'url': self.url,
            'info': self.info,
            'image': self.image,
            'summary': self.summary,
            'sort_id': int(self.sort_id),
            'hot_comment': self.hot_comment
        }

    def __str__(self) -> str:
        return f'{self.title}\n{self.info}\n{self.summary}\n{self.hot_comment}\n'


def spiderMovies():
    movies = []
    for tr in trs:
        tds = tr.find_all('td')
        date = tds[0].text.strip()
        if isNextMonth(date):
            title = tds[1].text.strip()
            print('spidering', title)
            link = tds[1].find('a').get('href')
            sort_id = tds[-1].text.strip().replace('人', '')
            movie = Movie(title, link, sort_id)
            movies.append(movie.toDict())
            time.sleep(1)
    movies.sort(key=lambda x: x['sort_id'], reverse=True)
    with open('movies.json', 'w', encoding='utf-8') as f:
        json.dump(movies, f, ensure_ascii=False, indent=4)

    # movies = json.load(open('movies.json', 'r', encoding='utf-8'))
    return movies
