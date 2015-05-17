
import time
import redis
import threading
import requests
import BeautifulSoup
import logging


logging.basicConfig(level=logging.INFO,
                    format='(%(threadName)-10s) %(message)s',
                    )


class Redis(object):

    def __init__(self, host='127.0.0.1', port=6379, db=0):
        super(Redis, self).__init__()
        self.__pool = redis.ConnectionPool(host=host, port=port, db=db)
        self.connection = redis.Redis(connection_pool=self.__pool)


class RedisStorage(Redis):

    def __init__(self):
        super(RedisStorage, self).__init__()

    def store(self, key, data):
        self.connection.set('_key', data)


class DataCruncher(threading.Thread):

    def __init__(self, web_data_queue, data_patterns):
        super(DataCruncher, self).__init__()
        self.web_data_queue = web_data_queue
        self.data_patterns = data_patterns

    def run(self):
        while True:
            data = self.web_data_queue.get()
            xml_data = BeautifulSoup.BeautifulSoup(requests.get(data).text)
            collected_data = {}
            for pattern in self.data_patterns:
                for element in pattern.get('elements'):
                    logging.info('Collecting data for %s', element)
                    collected_data[element] = xml_data.findAll(element)

            self.web_data_queue.task_done()


class Crawler(threading.Thread):

    def __init__(self, web_url_queue, web_data_queue):
        super(Crawler, self).__init__()
        self.web_data_queue = web_data_queue
        self.web_urls_queue = web_urls_queue

    def run(self):
        while True:
            page = self.web_urls_queue.get()
            self.web_data_queue.put(page)
            self.web_urls_queue.task_done()


from Queue import Queue
web_urls_queue = Queue()
web_data_queue = Queue()
if __name__ == '__main__':
    start = time.time()
    for i in range(5):
        crawler = Crawler(web_urls_queue, web_data_queue)
        crawler.setDaemon(True)
        crawler.start()

    for i in range(5):
        cruncher = DataCruncher(web_data_queue, [{'elements': ['a', 'span']}])
        cruncher.setDaemon(True)
        cruncher.start()

    for web in ["http://bing.com", "http://yahoo.com"]:
        web_urls_queue.put(web)

    web_urls_queue.join()
    web_data_queue.join()
    print logging.info('elapsed time: %s' % (time.time() - start))
