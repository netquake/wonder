from re import compile


class RegexTool(object):
    FLOAT_LOADER = compile('[\x00-\xff]*')

    @classmethod
    def read_float_from_string(cls, string):
        f = cls.FLOAT_LOADER.search(
            string
        ).group()

        return float(f) if f else 0.
