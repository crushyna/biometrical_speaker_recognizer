import configparser
import os


class BasicAuth:
    def __init__(self):
        config = configparser.ConfigParser()
        config.read(os.getcwd() + "/app/config.ini")
        self.login = config['BASIC_AUTH']['login']
        self.password = config['BASIC_AUTH']['pass']


