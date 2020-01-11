from scrapy.commands import ScrapyCommand

from ..persistence import db
from ..persistence.models import *


class Command(ScrapyCommand):
    default_settings = {'LOG_ENABLED': True}

    def short_desc(self):
        return '[Customed command] create all the tables in mysql'

    def run(self, args, opts):
        print('Creating tables...')

        db.create_all_tables()

        print('Done!')
