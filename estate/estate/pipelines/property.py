from ..persistence import db
from ..persistence.models import ApartmentPrice
from ..utils.regex_tool import RegexTool


class PropertyInfoPipeline(object):
    def process_item(self, item, spider):
        """Store apartments info into table
        """
        def get_room_number(s):
            i = s.find('室')
            return s[i-1:i] if i > 0 else 0

        new_apartment = ApartmentPrice(
            summary=item['name'],
            key_id=item['key_id'],
            source_type=item['source_type'],
            price=item['price'],
            area=RegexTool.read_float_from_string(item['area']),
            decoration=ApartmentPrice.get_decoration_type_from_string(item['fixtures']),
            layout=ApartmentPrice.get_layout_type_from_string(item['layout']),
            rooms=get_room_number(item['rooms']),
            region=item['region'],
            detail_url=item['url']
        )
        db.session.add(
            new_apartment
        )
        db.session.commit()

        return item
