from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    func
)

from ..database import db


class Contacts(db.Model):
    __tablename__ = 'contacts'

    profile_page = Column(
        String(512),
        primary_key=True,
        nullable=False,
        comment='Agents profile URL'
    )
    agent_name = Column(
        String(64), nullable=True, comment='Agents name'
    )
    agent_title = Column(
        String(128), nullable=True, comment='Agents title in company'
    )
    agency_name = Column(
        String(64), nullable=True, comment='Agency name'
    )
    agent_call = Column(
        String(64), nullable=True, comment='Agents phone/mobile'
    )
    license_company = Column(
        String(64), nullable=True, comment='Company license'
    )
    license_individual = Column(
        String(64), nullable=True, comment='Individual license'
    )
    number_of_sale = Column(Integer, nullable=True, default=0)
    number_of_rent = Column(Integer, nullable=True, default=0)
    agent_website = Column(
        String(512), nullable=True, comment='Agents website'
    )
    agent_email = Column(String(512), nullable=True, comment='Agents email')
    updated_at = Column(
        DateTime,
        nullable=False,
        server_default=func.now(),
        onupdate=func.now()
    )
