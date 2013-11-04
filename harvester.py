
import sys
import traceback
import time
import logging
from helper import Helper
from crop_loader import CropLoader



class Harvester(Helper):

    def __init__(self, field, crop):
        self.crop = crop
        self.field = field
        self.container = ''
        self.harvesting_delay = 10
        self.harvesting_time = 20
        self.crop_loader = CropLoader(self.field)
        super(Harvester, self).__init__(self.field, self.crop)

    def harvest(self):
        logging.info('harvesting: %s in %s' % (self.crop, self.field))
        self.container = self.filter_crop()
        self.crop_loader.container = self.container
        self.crop_loader.start()
        self.harvester_sleep()
        self.should_stop_harvesting()

    def should_stop_harvesting(self):
        if self.harvesting_time >= time.time() - self.harvesting_start_time:
            logging.info('Harvesting done!')
            sys.exit(0)

    def harvester_sleep(self):
        time.sleep(self.harvesting_delay)

    def start(self, harvesting_time=20, harvesting_delay=5):
        if self.field and self.crop:
            logging.info('harvesting for %s' % (self.field))
            self.harvesting_time = harvesting_time
            self.harvesting_delay = harvesting_delay
            try:
                self.harvesting_start_time = time.time()
                while True:
                    self.harvest()
            except Exception as ex:
                logging.error(traceback.format_exc())