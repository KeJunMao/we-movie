import matplotlib.pyplot as plt
import datetime
import requests
plt.rcParams['font.sans-serif'] = ['Arial Unicode MS']
plt.rcParams['axes.unicode_minus'] = False

last_month = (datetime.datetime.now() -
              datetime.timedelta(days=30)).replace(day=1).strftime("%Y-%m-%d")


def bar_chart(data):
    # 数据清洗
    # 创建一个空的列表
    x_data = []
    y_data = []
    # 遍历data列表
    for i in data:
        # 将每一个元素的boxoffice添加到x_data列表中
        x_data.append(int(i["boxoffice"]))
        # 将每一个元素的MovieName添加到y_data列表中
        y_data.append(i["MovieName"])
    # 创建一个条形图
    plt.title("上月电影票房")
    plt.barh(y_data, x_data)
    plt.tight_layout()
    # 保存
    path = f"photos/{last_month}电影票房.png"
    plt.savefig(path)
    return path


def get_last_month_data():
    url = "http://test.www.endata.com.cn/API/GetData.ashx"
    payload = f"startTime={last_month}&MethodName=BoxOffice_GetMonthBox"
    headers = {
        'Connection': 'keep-alive',
        'Accept': 'text/plain, */*; q=0.01',
        'X-Requested-With': 'XMLHttpRequest',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Origin': 'http://test.www.endata.com.cn',
        'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7,zh-TW;q=0.6'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    rjson = response.json()
    data = rjson["Data"]["Table"]
    data.sort(key=lambda x: x["boxoffice"])
    return data


def spiderBoxOffice():
    data = get_last_month_data()
    return {
        "data": data,
        "image": bar_chart(data)
    }
