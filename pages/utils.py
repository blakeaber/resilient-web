
from urllib.parse import urlparse, parse_qs


def parse_url_parameters(url, param=None):
    parsed = urlparse(url)
    available_params = parse_qs(parsed.query)
    if param in available_params:
        return parse_qs(parsed.query)[param][0]


def split_list_into_chunks(input_list, chunk_size):
    while len(input_list) < chunk_size:
        input_list.append(None)

    if len(input_list) % chunk_size:
        for _ in range(chunk_size - (len(input_list) % chunk_size)):
            input_list.append(None)

    return [
        input_list[i:i + chunk_size] 
        for i in range(0, len(input_list), chunk_size)
    ]
