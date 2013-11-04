import logging
from harvester import Harvester

if __name__ == '__main__':
    fields_and_crops = [{ 'http://www.irwinwong.com/blog/how-the-fuji-x-series-made-me-feel-inadequate/': [ 'src="([^"]+)"' ]}]
    for field_crops in fields_and_crops:
        for field, crops in field_crops.items():
            if isinstance(crops, list):
                for crop in crops:
                    harvester = Harvester(field, crop)
                    harvester.start()
