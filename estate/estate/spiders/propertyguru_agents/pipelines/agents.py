from ..persistence import db
from ..persistence.models import Contacts


db.create_all_tables()  # create sqlite3 file if doesn't exist.


class AgentsPipeline(object):
    def process_item(self, item, spider):
        """Store apartments info into table
        """
        print(item)

        pk_key = item['profile_page']
        contact = db.session.query(Contacts).get(pk_key)
        agent_name = item.get('agent_name')

        if contact:
            number_of_rent = item.get('number_of_rent')
            if number_of_rent:
                contact.number_of_rent = number_of_rent
            elif agent_name:
                contact.agent_name = agent_name
                contact.agent_title = item.get('agent_title')
                contact.agency_name = item.get('agency_name')
                contact.agent_call = item.get('agent_call')
                contact.license_company = item.get('license_company')
                contact.license_individual = item.get('license_individual')
                contact.agent_website = item.get('agent_website')
                contact.agent_email = item.get('agent_email')
                contact.number_of_sale = item.get('number_of_sale')

        else:
            contact = Contacts(
                profile_page=item.get('profile_page'),
                agent_name=item.get('agent_name', ''),
                agent_title=item.get('agent_title'),
                agency_name=item.get('agency_name'),
                agent_call=item.get('agent_call'),
                license_company=item.get('license_company'),
                license_individual=item.get('license_individual'),
                number_of_sale=item.get('number_of_sale'),
                number_of_rent=item.get('number_of_rent'),
                agent_website=item.get('agent_website'),
                agent_email=item.get('agent_email')
            )
            db.session.add(contact)

        db.session.commit()

        return item
