
import logging
import requests
import InputData
import BeautifulSoup
from multiprocessing import Pool
from collections import namedtuple

POOL_REQUIERD = 15
INPUT = namedtuple('INPUT', ('url', 'scrap_formats'))
logging.basicConfig(level=logging.INFO,
                    format='(%(threadName)-5s) %(processName)s %(message)s',
                    )


def parse_input(raw_input):
    return INPUT(raw_input.items()[0][0], raw_input.items()[0][1])


def get_page_xml_source(url):
    page = requests.get(url).text
    return BeautifulSoup.BeautifulSoup(page)


def scrap_data(input):
    xml_data = get_page_xml_source(input.url)
    scrap_data = []
    logging.info('scrapping: %s' % input.url)
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
    json_input = InputData.JSONInputData('input.json')
    pool = Pool(POOL_REQUIERD)
    inputs = [parse_input(raw_input) for raw_input in json_input.read()]
    results = [pool.apply_async(scrap_data, args=(input,)) for input in inputs]
    for r in results:
        logging.info(r.get())
