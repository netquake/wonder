"""
    Data handler of www.propertyguru.com.sg

"""
from re import compile

from scrapy import Field
from scrapy import Item
from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst


regex_email_partten_compiler = compile(
    r"""[\w!#$%&'*+/=?^_`{|}~-]+(?:\.[\w!#$%&'*+/=?^_`{|}~-]+)*@(?:[\w](?:[\w-]*[\w])?\.)+[\w](?:[\w-]*[\w])?"""  # noqa
)

regex_integer_partten_compiler = compile(
    r"""^[1-9]\d*"""
)


class AgentContactLoader(ItemLoader):
    default_output_processor = TakeFirst()


def strip_first(values):
    first = values[0]

    if first:
        first = first.replace('\r', '').replace('\n', '')

        return first.strip()
    else:
        return None


def get_license_company(values):
    first = values[0]

    return strip_first([first])


def get_license_individual(values):
    first = values[1]

    return strip_first([first])


def get_email(values):
    v = regex_email_partten_compiler.search(
        values[0]
    )

    return v.group() if v else None


def get_number_of_sale(values):
    v = regex_integer_partten_compiler.search(
        values[0]
    )

    return int(v.group()) if v else 0


def get_number_of_rent(values):
    v = regex_integer_partten_compiler.search(
        values[0]
    )

    return int(v.group()) if v else 0


class AgentContact(Item):
    profile_page = Field()
    agent_name = Field(output_processor=strip_first)
    agent_title = Field(output_processor=strip_first)
    agency_name = Field(output_processor=strip_first)
    agent_call = Field(output_processor=strip_first)
    license_company = Field(output_processor=get_license_company)
    license_individual = Field(output_processor=get_license_individual)
    number_of_sale = Field(output_processor=get_number_of_sale)
    number_of_rent = Field(output_processor=get_number_of_rent)
    agent_website = Field(output_processor=strip_first)
    agent_email = Field(output_processor=get_email)
