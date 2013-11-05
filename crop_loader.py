
from warehouse import Warehouse

from logger import logger

class CropLoader(object):

    def __init__(self, field):
        self.warehouse = Warehouse()
        self.container = None
        self.from_field = field

    def store_into_warehouse(self):
        logger.debug('Storing %s => %s' % (self.from_field, self.container))
        self.warehouse.store(self.from_field, self.container)

    def start(self):
        if self.container:
            self.store_into_warehouse()