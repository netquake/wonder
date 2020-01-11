from ..persistence.models import ApartmentPrice


class PropertyInfoPipeline(object):
    def process_item(self, item, spider):
        print('....................................')
        print(dict(item))
        return item
