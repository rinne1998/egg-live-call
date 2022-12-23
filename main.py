import http.client
from codecs import encode
import json
import time
import re
import random

sentences = [
    "\爱哥/\爱哥/\爱哥/",
    "这是爱哥，ta是最棒的！",
    "\中国绊爱，无所替代/"
]


boundary = 'wL36Yn8afVp8Ag7AmP8qZ0SA4n1v9T'
csrf_regex = r'bili_jct=(.*?);'
conn = http.client.HTTPSConnection("api.live.bilibili.com")


def generateRequest(text, csrf_token):
    dataList = []
    dataList.append(encode('--' + boundary))
    dataList.append(encode('Content-Disposition: form-data; name=bubble;'))

    dataList.append(encode('Content-Type: {}'.format('text/plain')))
    dataList.append(encode(''))

    dataList.append(encode("5"))
    dataList.append(encode('--' + boundary))
    dataList.append(encode('Content-Disposition: form-data; name=msg;'))

    dataList.append(encode('Content-Type: {}'.format('text/plain')))
    dataList.append(encode(''))

    dataList.append(encode(text))
    dataList.append(encode('--' + boundary))
    dataList.append(encode('Content-Disposition: form-data; name=color;'))

    dataList.append(encode('Content-Type: {}'.format('text/plain')))
    dataList.append(encode(''))

    dataList.append(encode("16777215"))
    dataList.append(encode('--' + boundary))
    dataList.append(encode('Content-Disposition: form-data; name=mode;'))

    dataList.append(encode('Content-Type: {}'.format('text/plain')))
    dataList.append(encode(''))

    dataList.append(encode("4"))
    dataList.append(encode('--' + boundary))
    dataList.append(encode('Content-Disposition: form-data; name=fontsize;'))

    dataList.append(encode('Content-Type: {}'.format('text/plain')))
    dataList.append(encode(''))

    dataList.append(encode("25"))
    dataList.append(encode('--' + boundary))
    dataList.append(encode('Content-Disposition: form-data; name=rnd;'))

    dataList.append(encode('Content-Type: {}'.format('text/plain')))
    dataList.append(encode(''))
    t = str(int(time.time()))
    dataList.append(encode(t))
    dataList.append(encode('--' + boundary))
    dataList.append(encode('Content-Disposition: form-data; name=roomid;'))

    dataList.append(encode('Content-Type: {}'.format('text/plain')))
    dataList.append(encode(''))

    dataList.append(encode("21712406"))
    dataList.append(encode('--' + boundary))
    dataList.append(encode('Content-Disposition: form-data; name=csrf;'))

    dataList.append(encode('Content-Type: {}'.format('text/plain')))
    dataList.append(encode(''))

    dataList.append(encode(csrf_token))
    dataList.append(encode('--' + boundary))
    dataList.append(encode('Content-Disposition: form-data; name=csrf_token;'))

    dataList.append(encode('Content-Type: {}'.format('text/plain')))
    dataList.append(encode(''))

    dataList.append(encode(csrf_token))
    dataList.append(encode('--'+boundary+'--'))
    dataList.append(encode(''))
    return b'\r\n'.join(dataList)


cookies = []
with open("./cookie.txt", 'r', encoding='utf-8') as f:
    count = 0
    for i in f.readlines():
        match_regex = re.findall(csrf_regex, i)
        if len(match_regex) > 0:
            cookies.append((i.replace("\n",""), match_regex[0]))
            print(cookies)
            count += 1
    print(f"共载入{count}个账号")
while True:
    times = 0
    for k in cookies:
        sentence = random.choice(sentences)
        payload = generateRequest(sentence, k[1])
        headers = {
            'authority': 'api.live.bilibili.com',
            'accept': '*/*',
            'accept-language': 'zh-CN,zh;q=0.9',
            'cache-control': 'no-cache',
            'cookie': k[0],
            'origin': 'https://live.bilibili.com',
            'pragma': 'no-cache',
            'referer': 'https://live.bilibili.com/blanc/21712406?liteVersion=true',
            'sec-ch-ua': '"Not_A Brand";v="99", "Google Chrome";v="109", "Chromium";v="109"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-site',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
            'Content-type': 'multipart/form-data; boundary={}'.format(boundary),
            "Connection":"Close",
        }
        conn.request("POST", "/msg/send", payload, headers)
        res = conn.getresponse()
        data = res.read()
        result = json.loads(data.decode("utf-8"))
        if result['code'] == 0:
            print(f"发送成功：{sentence}")
        else:
            print(f"发送失败：{result['message']}，请重新配置cookie！")
        times += 1
        time.sleep(1)
    time.sleep(5 if times < 3 else 3)
