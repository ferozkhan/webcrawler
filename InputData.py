
import json


class InputData(object):
    def read(self):
        raise NotImplementedError


class JSONInputData(InputData):
    def __init__(self, path):
        super(JSONInputData, self).__init__()
        self.path = path

    def read(self):
        with open(self.path) as f:
            return json.loads(f.read())
