from ..persistence import db
from ..persistence.models import ApartmentPrice
from ..utils.regex_tool import RegexTool


class PropertyInfoPipeline(object):
    def process_item(self, item, spider):
        """Store apartments info into table
        'rooms': '3室2厅', 'layout': '南 北', 'fixtures': '精装'
        """
        new_apartment = ApartmentPrice(
            summary=item['name'],
            price=item['price'] // 100,
            area=RegexTool.read_float_from_string(item['area']),
            decoration=0,
            layout=0,
            rooms=1,
            region=item['region'],
            detail_url=item['url']
        )
        db.session.add(
            new_apartment
        )
        db.session.commit()

        return item
