
import time
import redis
import cjson
import requests
import traceback
import BeautifulSoup
from logger import logger


class RedisStorage(object):
    
    def __init__(self, host='127.0.0.1', port=6379, db=0):
        super(RedisStorage, self).__init__()
        self__pool = redis.ConnectionPool(host=self.host, port=self.port, db=self.db)
        self.connection = redis.Redis(connection_pool=self.__pool)
            

class Storage(RedisStorage):

    def __init__(self):
        super(RedisStorage, self).__init__()

    def store(self, key, data):
        _key = ':'.join(key)
        self.connection.set(_key, data)


class Crawler(object):

    def __init__(self, pages, data_patterns):
        super(Crawler, self).__init__()
        self.pages = pages
        self.data_patterns = data_patterns
        self.storage = Storage()
        self.container = {}
        self.links = []

    def crawl(self, callback=None):
        if self.pages and self.data_patterns:
            try:
                _data, _attrs = [], {}
                for page in self.pages:
                    __page_html = requests.get(page).text
                    __page_xml = BeautifulSoup.BeautifulSoup(__page_html)
                    for pattern in self.data_patterns:
                        if 'element' not in pattern:
                            raise Exception('"Element" is missing')

                        data = __page_xml.findAll([pattern], _attrs)
                        for d in data:
                            print d.text

                        # self.storage.store((page, pattern), _data)
            except Exception as e:
                raise e



if __name__ == '__main__':
    c = Crawler(['ANY_URL'], [{'element':['span']}])
    c.crawl()

