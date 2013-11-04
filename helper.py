
import re
import requests
import logging

class Helper(object):

    def __init__(self, field, crop):
        self.field = field
        self.crop = crop

    def raw_crop(self):
        f = requests.get(self.field)
        return f.text

    def filter_crop(self):
        logging.info('filtering crop')
        return re.findall(self.crop, self.raw_crop())

