from lxml import etree
import requests

class Login():
    def __init__(self):
        self.header = {
            'Referer': 'https://github.com',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2957.133 Safari.537.36',
            'Host': 'github.com'
        }
        self.loginUrl = 'https://github.com/login'
        self.postUrl = 'https://github.com/session'
        self.loginedUrl = 'https://github.com/settings/profile'
        self.session = requests.session()

    def token(self):
        response = self.session.get(self.loginUrl, headers = self.header)
        selector = etree.HTML(response.text)
        token = selector.xpath('//div//input[2]/@value')[0]

        return token


    def login(self, email, password):
        postData = {
            'commit': 'Sign in',
            'utf-8': '',
            'authenticity_token': self.token(),
            'login': email,
            'password': password
        }

        response = self.session.post(self.postUrl, data = postData, headers = self.header)
        if response.status_code == 200:
            self.dynamics(response.text)

        response = self.session.get(self.loginUrl, headers =  self.header)
        if response.status_code == 200:
            self.profile(response.text)

    def dynamics(self, html):
        selector = etree.HTML(html)
        dynamics = selector.xpath('//div[contains(@class, "news")]//div[contains(@class, "alert")]')
        for item in dynamics:
            dynamic = ' '.join(item.xpath('//div[@class="title"]//text()')).strip()
            print(dynamic)

    def profile(self, html):
        selector = etree.HTML(html)
        name = selector.xpath('//input[@id="user_profile_name"]/@value')[0]
        email = selector.xpath('//select[@id="user_profile_email"]/option[@value!=""]/text()')
        print(name, email)

if __name__ == '__main__':
    email = 'email'
    password = 'password'
    login = Login()
    login.login(email, password)