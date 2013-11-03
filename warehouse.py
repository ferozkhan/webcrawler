
import redis
import cjson
import logging


class Warehouse(object):

    def __init__(self, host='127.0.0.1', port=6379, db=0):
        self.log = logging.getLogger('Warehouse')
        self.host = host
        self.port = port
        self.db = db
        self.slot_available = True
        self.storage = redis.ConnectionPool(host=self.host, port=self, db=self.db)

    def get_slot(self):
        if self.slot_available:
            return redis.Redis(connection_pool=self.storage)

    def store(self, block, crop):
        slot = self.get_slot()
        slot.set(block, cjson.dumps(crop))




