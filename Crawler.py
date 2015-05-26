
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
    return BeautifulSoup.BeautifulSoup(requests.get(url).text)


def scrap_data(input):
    xml_data = get_page_xml_source(input.url)
    logging.info('scrapping: %s' % input.url)
    for sf in input.scrap_formats:
        try:
            element = sf.pop('element')
            return ((input.url, element, sf),
                    [d.getText(' ')
                     for d in xml_data.findAll(element, attrs=sf)]
                    )
        except KeyError, e:
            logging.error(
                "Key: '{}' must be provided. URL: {}".format(e, input.url)
            )


if __name__ == '__main__':
    pool = Pool(POOL_REQUIERD)
    json_input = InputData.JSONInputData('input.json')
    inputs = [parse_input(raw_input) for raw_input in json_input.read()]
    results = [pool.apply_async(scrap_data, args=(input,)) for input in inputs]
    pool.close()
    pool.join()
    for r in results:
        logging.info(r.get())
