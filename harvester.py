
import sys
import traceback
import time
from helper import Helper
from crop_loader import CropLoader
from logger import logger

from celery import Celery
celery = Celery('harvester', backend='amqp', broker='amqp://')
celery.config_from_object('celeryconfig')

class Harvester(object):

    def __init__(self, field, crop):
        self.crop = crop
        self.field = field
        self.container = ''
        self.crop_loader = CropLoader(self.field)
        self.helper = Helper(self.field, self.crop)

    def harvest(self):
        logger.info('Starting harvesting at %s for %s' % (self.field, self.crop))
        logger.debug('harvesting: %s in %s' % (self.crop, self.field))
        self.container = self.helper.filter_crop()
        self.crop_loader.container = self.container
        self.crop_loader.start()

    def start(self):
        if self.field and self.crop:
            try:
                self.harvest()
            except Exception as ex:
                logger.error(traceback.format_exc())
