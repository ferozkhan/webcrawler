
import redis


class Redis(object):

    def __init__(self, host='127.0.0.1', port=6379, db=0):
        super(Redis, self).__init__()
        self.__pool = redis.ConnectionPool(host=host, port=port, db=db)
        self.connection = redis.Redis(connection_pool=self.__pool)


class RedisStorage(Redis):

    def __init__(self):
        super(RedisStorage, self).__init__()

    def store(self, key, data):
        self.connection.set('_key', data)
