

import time
import json
import requests
import BeautifulSoup
import logging
from collections import namedtuple
from multiprocessing import Pool

THREAD_REQUIERD = 5

logging.basicConfig(level=logging.INFO,
                    format='(%(threadName)-5s) %(message)s',
                    )

INPUT = namedtuple('INPUT', ('url', 'scrap_formats'))


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


def parse_input(raw_input):
    return INPUT(raw_input.items()[0][0], raw_input.items()[0][1])


def get_page_xml_source(url):
    page = requests.get(url).text
    return BeautifulSoup.BeautifulSoup(page)


def scrap_data(input):
    xml_data = get_page_xml_source(input.url)
    scrap_data = []
    for sf in input.scrap_formats:
        if isinstance(sf, dict):
            sub_scrap_data = {
                sf.items()[0]: [d.getText() for d in xml_data.findAll(attrs=sf)]
            }
        else:
            sub_scrap_data = {
                sf: [d.getText() for d in xml_data.findAll(sf)]
            }
        scrap_data.append(sub_scrap_data)
    return scrap_data


if __name__ == '__main__':
    json_input = JSONInputData('input.json')
    pool = Pool(5)
    inputs = [parse_input(raw_input) for raw_input in json_input.read()]
    start = time.time()
    result = pool.map(scrap_data, inputs)
    print 'elapsed time %10.7f' % (time.time() - start)
