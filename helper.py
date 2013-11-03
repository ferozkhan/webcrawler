
import re
import requests

class Helper(object):

    def __init__(self, field, crop):
        self.log = logging.getLogger('Helper')
        self.field = field
        self.crop = crop

    def raw_crop(self):
        f = requests.get(self.field)
        return f.text

    def filter_crop(self):
        return re.findall(self.crop, self.raw_crop())

