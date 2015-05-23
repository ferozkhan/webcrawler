

import time
import json
import threading
import requests
import BeautifulSoup
import logging

THREAD_REQUIERD = 5

logging.basicConfig(level=logging.INFO,
                    format='(%(threadName)-10s) %(message)s',
                    )


class InputData(object):
    def read(self):
        raise NotImplementedError


class JSONInputData(InputData):
    def __init__(self, path):
        super(JSONInputData, self).__init__()
        self.path = path

    def read(self):
        with open(self.path) as f:
            return json.loads(f.read())


class DataCrawler(threading.Thread):

    def __init__(self, web_xml_queue):
        super(DataCrawler, self).__init__()
        self.web_xml_queue = web_xml_queue

    def run(self):
        while True:
            xml_data, elements = self.web_xml_queue.get()
            _data = {}
            for e in elements:
                if isinstance(e, dict):
                    _data[e.items()[0][1]] = [x.getText() for x in xml_data.findAll(attrs=e)]
                else:
                    _data[e] = xml_data.findAll(e)
            print _data
            self.web_xml_queue.task_done()


class XMLData(threading.Thread):

    def __init__(self, web_data_queue, web_xml_queue):
        super(XMLData, self).__init__()
        self.web_data_queue = web_data_queue
        self.web_xml_queue = web_xml_queue

    def run(self):
        while True:
            url, elements = self.web_data_queue.get()
            logging.info('Processing data from %s for %s' % (url, elements))
            xml_data = BeautifulSoup.BeautifulSoup(requests.get(url).text)
            self.web_xml_queue.put((xml_data, elements))
            self.web_data_queue.task_done()


class Crawler(threading.Thread):

    def __init__(self, web_url_queue, web_data_queue):
        super(Crawler, self).__init__()
        self.web_data_queue = web_data_queue
        self.web_urls_queue = web_urls_queue

    def run(self):
        while True:
            meta = self.web_urls_queue.get()
            url, elements = meta.items()[0]
            self.web_data_queue.put((url, elements))
            self.web_urls_queue.task_done()


from Queue import Queue
web_urls_queue = Queue()
web_data_queue = Queue()
web_xml_queue = Queue()

if __name__ == '__main__':
    start = time.time()
    threads = []
    for i in range(THREAD_REQUIERD):
        crawler = Crawler(web_urls_queue, web_data_queue)
        crawler.setDaemon(True)
        threads.append(crawler)
        crawler.start()

        cruncher = DataCrawler(web_xml_queue)
        cruncher.setDaemon(True)
        threads.append(cruncher)
        cruncher.start()

        cruncher = XMLData(web_data_queue, web_xml_queue)
        cruncher.setDaemon(True)
        threads.append(cruncher)
        cruncher.start()

    json_data = JSONInputData('input.json')
    for _input in json_data.read():
        web_urls_queue.put(_input)

    web_urls_queue.join()
    web_data_queue.join()
    web_xml_queue.join()

    print logging.info('elapsed time: %s' % (time.time() - start))
