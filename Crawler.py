import logging
import requests
import InputData
import BeautifulSoup
from multiprocessing import Pool
from collections import namedtuple

INPUT = namedtuple('INPUT', ('url', 'scrap_formats'))
logging.basicConfig(level=logging.INFO,
                    format='(%(threadName)-5s) %(processName)s %(message)s',
                    )


def prepare_input(data):
    """

    :rtype : INPUT(url, scrap_formats)
    """
    return INPUT(data.items()[0][0], data.items()[0][1])


def get_page_xml_source(url):
    return BeautifulSoup.BeautifulSoup(requests.get(url).text)


def scrap_data(data):
    xml_data = get_page_xml_source(data.url)
    logging.info('scrapping: %s' % data.url)
    for sf in data.scrap_formats:
        try:
            element = sf.pop('element')
            separator = sf.pop('separator') if 'separator' in sf else ''
            return ((data.url, element, sf),
                    [d.getText(separator)
                     for d in xml_data.findAll(element, attrs=sf)]
                    )
        except KeyError, e:
            logging.error(
                "Key: '{}' must be provided. URL: {}".format(e, data.url)
            )


def scrapy_do(scrap_formats_file_name, pool_required=5):
    scrap_formats_file = InputData.JSONInputData(scrap_formats_file_name)
    scraps_async_result = []
    pool = Pool(pool_required)
    for scrap_format in scrap_formats_file.read():
        scraps_async_result.append(pool.apply_async(scrap_data, args=(prepare_input(scrap_format), )))


if __name__ == '__main__':
    scrapy_do('input.json')
