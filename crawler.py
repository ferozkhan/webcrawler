
import redis
import cjson
import requests
import BeautifulSoup
from logger import logger

class Storage(object):

    def __init__(self, host='127.0.0.1', port=6379, db=0):
        self.host = host
        self.port = port
        self.db = db
        self.connection_pool = redis.ConnectionPool(host=self.host, port=self.port, db=self.db)
        self.connection = redis.Redis(connection_pool=self.connection_pool)

    def store(self, key, data):
        _key = ':'.join(key)
        self.connection.set(_key, data)

class Crawler(object):

    def __init__(self, pages, data_patterns):
        self.pages = pages
        self.data_patterns = data_patterns
        self.storage = Storage()
        self.container = {}

    def crawl(self):
        if self.pages and self.data_patterns:
            try:
                _data = []
                for page in self.pages:
                    __page_html = requests.get(page).text
                    __page_xml = BeautifulSoup.BeautifulSoup(__page_html)
                    for pattern in self.data_patterns:
                        for data in __page_xml.findAll(pattern):
                            _data.append(data)
                        self.storage.store((page, pattern), _data)
            except Exception as e:
                raise e



if __name__ == '__main__':
    c = Crawler(['http://in.yahoo.com', 'http://google.com/'], ['img', 'a'])
    c.crawl()
