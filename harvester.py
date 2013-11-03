
import traceback
import logging
from helper import Helper
from crop_loader import CropLoader


class Harvester(Helper):

    def __init__(self, field, crop):
        self.log = logging.getLogger('Harvester')
        self.crop = crop
        self.field = field
        self.container = ''
        self.crop_loader = CropLoader(self.field)
        super(Harvester, self).__init__(self.field, self.crop)

    def harvest(self):
        self.log.info('harvesting: %s in %s' % (self.crop, self.field))
        self.container = self.filter_crop()
        self.crop_loader.container = self.container

    def start(self):
        if self.field and self.crop:
            try:
                self.harvest()
                self.crop_loader.start()
            except Exception as ex:
                self.log.error(traceback.format_exc())