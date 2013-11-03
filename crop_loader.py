
from warehouse import Warehouse


class CropLoader(object):

    def __init__(self, slot):
        self.log = logging.getLogger('CropLoader')
        self.warehouse = Warehouse()
        self.container = None
        self.slot = slot

    def store_into_warehouse(self):
        self.warehouse.store(self.slot, self.container)

    def start(self):
        if self.container:
            self.store_into_warehouse()