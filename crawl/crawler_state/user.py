class User:
    def __init__(self, webname, username, link, title, md5):
        self.webname = webname
        self.username = username
        self.link = link
        self.title = title
        self.md5 = md5

        @property
        def webname(self):
            return self.webname

        @webname.setter
        def webname(self, webname):
            self.webname = webname

        @property
        def username(self):
            return self.username

        @username.setter
        def username(self, username):
            self.username = username

        @property
        def link(self):
            return self.link

        @link.setter
        def link(self, link):
            self.link = link

        @property
        def title(self):
            return self.title

        @title.setter
        def title(self, title):
            self.title = title

        @property
        def md5(self):
            return self.md5

        @md5.setter
        def md5(self, md5):
            self.md5 = md5