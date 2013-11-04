
import redis
import cjson
import logging
from datetime import datetime


class Warehouse(object):

    def __init__(self, host='127.0.0.1', port=6379, db=0):
        self.host = host
        self.port = port
        self.db = db
        self.storage = redis.ConnectionPool(host=self.host, port=self.port, db=self.db)
        self.storage_slot = redis.Redis(connection_pool=self.storage)

    def store(self, from_field, crop):
        logging.info('storing %s => %s' % (from_field, crop))
        self.storage_slot.set(from_field, cjson.encode(crop))
        self.update_known_field(from_field)

    def update_known_field(self, from_field):
        known_field = self.storage_slot.get('known_field')
        if known_field:
            known_field = cjson.decode(known_field)
            if isinstance(known_field, dict):
                known_field[from_field] = str(datetime.now())
            else:
                raise TypeError('known field is not a dict.')
        else:
            known_field = {}
            known_field[from_field] = str(datetime.now())
        self.storage_slot.set('known_field', cjson.encode(known_field))


