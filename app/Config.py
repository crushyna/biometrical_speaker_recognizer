import configparser


class BasicAuth:
    def __init__(self):
        config = configparser.ConfigParser()
        config.read("config.ini")
        self.login = config['BASIC_AUTH']['login']
        self.password = config['BASIC_AUTH']['pass']
