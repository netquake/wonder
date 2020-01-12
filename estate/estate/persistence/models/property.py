from sqlalchemy import (
    Column, text,
    SmallInteger, Integer,
    Float, String, TIMESTAMP
)

from ..database import db


class ApartmentPrice(db.Model):
    __tablename__ = 'apartment_price'
    __table_args__ = {'schema': 'wonder'}

    TYPE_LAYOUT_UNKNOW = 0
    TYPE_LAYOUT_SOUTH_NORTH = 1
    TYPE_LAYOUT_ALL_SOUTH = 2
    TYPE_LAYOUT_ALL_NORTH = 3

    TYPE_DECORATION_UNKNOW = 0
    TYPE_DECORATION_BLANK = 1
    TYPE_DECORATION_PAPERBACK = 2
    TYPE_DECORATION_HARDBACK = 3
    TYPE_DECORATION_LUXURY = 4

    id = Column(Integer, primary_key=True, autoincrement=True)
    key_id = Column(String(64), nullable=False, index=True, comment='key id of property record')
    summary = Column(String(512), nullable=False, comment='brief description')
    source_type = Column(SmallInteger, nullable=False, index=True, comment='0:unknow 1:Lianjia')
    village_name = Column(String(128), nullable=True, index=True, comment='XiaoQu Name')
    price = Column(Integer, nullable=False, comment='RMB(Wan Yuan)')
    area = Column(Float, nullable=False)
    decoration = Column(SmallInteger, nullable=False, default=0, comment='0:unknow 1:blank 2:paperback 3:hardback 4:luxury')
    layout = Column(SmallInteger, nullable=False, default=0, comment='0:unknow 1:南北 2:两南 3:两北')
    rooms = Column(SmallInteger, nullable=False, default=1, comment='room number of apartment')
    region = Column(String(128), nullable=True, comment='location name, like "七宝 陆家嘴 张江"')
    detail_url = Column(String(512), nullable=True)
    created_at = Column(TIMESTAMP, nullable=False, server_default=text('CURRENT_TIMESTAMP'))
    updated_at = Column(TIMESTAMP, nullable=False, server_default=text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'))

    @classmethod
    def get_layout_type_from_string(cls, s):
        if '南' in s and '北' in s:
            return cls.TYPE_LAYOUT_SOUTH_NORTH
        elif '南' in s and '北' not in s:
            return cls.TYPE_LAYOUT_ALL_SOUTH
        elif '南' not in s and '北' in s:
            return cls.TYPE_LAYOUT_ALL_NORTH
        else:
            return cls.TYPE_LAYOUT_UNKNOW

    @classmethod
    def get_decoration_type_from_string(cls, s):
        if '毛' in s or '柸' in s:
            return cls.TYPE_DECORATION_BLANK
        elif '简' in s:
            return cls.TYPE_DECORATION_PAPERBACK
        elif '精' in s:
            return cls.TYPE_DECORATION_HARDBACK
        elif '豪' in s:
            return cls.TYPE_DECORATION_LUXURY
        else:
            return cls.TYPE_LAYOUT_UNKNOW
