from re import search, compile
from time import time, sleep

from requests import request

_domain = 'https://api.datastream.org'
_location_filter_regex = compile('^Id| Id|^LocationId| LocationId')
_rate_limit_seconds = 0.5
_rate_limit_timestamp = 0

_default_params = {'$top': 10000}
_request_headers = {'Accept': 'application/vnd.api+json'}


def set_api_key(key: str):
    _request_headers.update({'x-api-key': key})


def metadata(params: dict):
    path = '/v1/odata/v4/Metadata'
    response = _fetch(path, params)

    if _is_count_request(params):
        return next(response)
    else:
        return response


def locations(params: dict):
    path = '/v1/odata/v4/Locations'
    response = _fetch(path, params)

    if _is_count_request(params):
        return next(response)
    else:
        return response


def observations(params: dict):
    path = '/v1/odata/v4/Observations'

    if _is_count_request(params):
        return next(_fetch(path, params))
    else:
        return _partition_request(path, params)


def records(params: dict):
    path = '/v1/odata/v4/Records'

    if _is_count_request(params):
        return next(_fetch(path, params))
    else:
        return _partition_request(path, params)


def _request(url, params=None):
    _rate_limit()

    res = request(method='GET',
                  url=url,
                  params=params,
                  headers=_request_headers,
                  timeout=60)

    if res.status_code == 429:
        # too many requests, try again with rate limiting
        return _request(url, params)

    res.raise_for_status()
    return res


def _fetch(path, params):
    url = f'{_domain}{path}'
    params = _default_params | params
    prefetch = _request(url, params).json()
    next_link = None

    while prefetch or next_link:
        response = prefetch or _request(url=next_link).json()

        prefetch = None
        next_link = response.get('@odata.nextLink', None)

        data = response.get('value', None)
        if isinstance(data, list):
            for item in data:
                yield item
        else:
            yield data


def _partition_request(path, params):
    request_filter = params.get('$filter', '')

    if search(_location_filter_regex, request_filter):
        # If filtering by specific Id or LocationId, no need to partition
        yield from _fetch(path, params)
    else:
        all_locations = locations({
            '$select': 'Id',
            '$filter': request_filter
        })
        for location in all_locations:
            location_filter = f'LocationId eq {location["Id"]}'
            location_filter += f' and {request_filter}' if request_filter else ''
            params = params | {'$filter': location_filter}
            yield from _fetch(path, params)


def _is_count_request(params):
    return params.get('$count', 'false') == 'true'


def _rate_limit():
    global _rate_limit_timestamp

    if time() < _rate_limit_timestamp:
        sleep(_rate_limit_seconds)

    _rate_limit_timestamp = time() + _rate_limit_seconds
