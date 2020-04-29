
from urllib.parse import urlparse, parse_qs


def parse_url_parameters(url, param=None):
    parsed = urlparse(url)
    if param:
        return parse_qs(parsed.query)[param][0]
    else:
        return parse_qs(parsed.query)
