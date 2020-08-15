from scrapy.commands import ScrapyCommand

from ..persistence import db
from ..persistence.models import *


class Command(ScrapyCommand):
    default_settings = {'LOG_ENABLED': True}

    def short_desc(self):
        return '[Customed command] drop all the tables in mysql'

    def run(self, args, opts):
        print('Dropping tables...')

        db.drop_all_tables()

        print('Done!')
