
import re
import urllib
import BeautifulSoup as bs
import requests

from logger import logger

class Helper(object):

    def __init__(self, field, crop):
        self.field = field
        self.crop = crop

    def filter_crop(self):
        _raw_crop = urllib.urlopen(self.field)
        _arranged_raw_crop = bs.BeautifulSoup(_raw_crop)
        return _arranged_raw_crop.findAll(self.crop)

