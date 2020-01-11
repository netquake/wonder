from ..utils import RandomAgent


class RandomUserAgent(object):
    """Randomly rotate user agents based on a list of predefined ones
    """
    def process_request(self, request, spider):
        request.headers.setdefault(
            'User-Agent', RandomAgent.random_agent()
        )
