# 引入需要的模块
import requests
import re

# 定义CETWORD类，实现连接百词斩网站，模拟登陆、答题并抓取图片、音频等资源。


class CETWORD:
    # 基本属性
    username = ''
    password = ''
    token = ''
    cookies = ''
    words = []
    sentences = []
    word_audio_urls = []
    sentence_audio_urls = []
    image_urls = []
    id = 0
    topic_id = []

    # 重载构造函数，定义登陆百词斩网站的用户名、密码、认证码
    def __init__(self, _username, _password, _token):
        self.username = _username
        self.password = _password
        self.token = _token
        self.id = 0

    # 登陆百词斩网站
    def login(self):
        payload = {'email': self.username, 'raw_pwd': self.password}
        r = requests.post('http://www.baicizhan.com/login', data=payload)
        self.cookies = r.cookies

    # 进入单词界面并获取图片、视频等链接地址
    def slash(self):
        cookie = dict(auth_token=self.token)
        r = requests.get('http://www.baicizhan.com/words/slash', cookies=cookie)
        html = r.text
        self.regex(html)

    # 通过正则表达式获取资源
    def regex(self, html):
        self.words = re.findall('word_audio_name":"(.*?).mp3"', html)
        self.sentences = re.findall('"sentence":"(.*?)"', html)
        self.word_audio_urls = re.findall('word_voice":"(.*?)"', html)
        self.sentence_audio_urls = re.findall('audio_file":"(.*?)"', html)
        self.image_urls = re.findall('thumbnail_image":"(.*?)"', html)
        self.topic_id = re.findall('topic_id":(.*?),"', html)

    # 下载音频、图片文件
    def download(self):
        for count in range(0, self.words.__len__()):
            r = requests.get(self.image_urls[count * 4], stream=True)
            c = r.content
            try:
                with open('images/' + self.words[count] + '.jpg', 'wb') as jpg:
                    jpg.write(c)
            except IOError:
                pass
            finally:
                jpg.close()
            r = requests.get(self.word_audio_urls[count], stream=True)
            c = r.content
            try:
                with open('wordaudios/' + self.words[count] + '.mp3', 'wb') as mp3:
                    mp3.write(c)
            except IOError:
                pass
            finally:
                mp3.close()
            r = requests.get(self.sentence_audio_urls[count], stream=True)
            c = r.content
            try:
                with open('sentenceaudios/' + self.words[count] + '.mp3', 'wb') as mp3:
                    mp3.write(c)
            except IOError:
                pass
            finally:
                mp3.close()

    # 提交JSON到百词斩网站
    def submit(self):
        count = 1
        cookie = dict(auth_token=self.token)
        for item in self.topic_id[::-1]:
            if count % 4 == 0:
                payload = {'word_topic_id': str(item)}
                requests.post('http://www.baicizhan.com/words/pass.json', cookies=cookie, data=payload)
            count += 1

    # 实现翻页
    def next(self):
        cookie = dict(auth_token=self.token)
        requests.get('http://www.baicizhan.com/users/get_more_words', cookies=cookie)

# 测试
cet = CETWORD('mark@gmail.com', '1314512', '33882154%3A9a33737597992402abe627e088f010a3a5bd0bb2')
cet.login()
cet.id = 3012
flag = True
while flag:
    cet.next()
    cet.slash()
    cet.download()
    cet.submit()
    cet.slash()
    cet.download()
    cet.submit()
    if cet.id > 3069:
        flag = False
