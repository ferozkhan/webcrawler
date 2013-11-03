

from harvester import Harvester

if __name__ == '__main__':
    fields_and_crops = []
    for field_crops in fields_and_crops:
        for field, crops in field_crops.items():
            if isinstance(crops, list):
                for crop in crops:
                    harvester = Harvester(field, crop)
                    while True:
                        harvester.start()
