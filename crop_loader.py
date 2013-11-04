
from warehouse import Warehouse
import logging

class CropLoader(object):

    def __init__(self, field):
        self.warehouse = Warehouse()
        self.container = None
        self.from_field = field

    def store_into_warehouse(self):
        self.warehouse.store(self.from_field, self.container)

    def start(self):
        if self.container:
            self.store_into_warehouse()