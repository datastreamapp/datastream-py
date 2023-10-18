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
    return _fetch(path='/v1/odata/v4/Metadata', params=params)


def locations(params: dict):
    return _fetch(path='/v1/odata/v4/Locations', params=params)


def observations(params: dict):
    return _partition_request(path='/v1/odata/v4/Observations', params=params)


def records(params: dict):
    return _partition_request(path='/v1/odata/v4/Records', params=params)


def _request(url, params=None):
    _rate_limit()

    res = request(method='GET',
                  url=url,
                  params=params,
                  headers=_request_headers)

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

        data = response.get('value', [])
        for item in data:
            yield item


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


def _rate_limit():
    global _rate_limit_timestamp

    if time() < _rate_limit_timestamp:
        # print(f'rate limiting; current: {time()}; next: {_rate_limit_timestamp};'
        #       f' sleeping for {_rate_limit_seconds} seconds')
        sleep(_rate_limit_seconds)

    _rate_limit_timestamp = time() + _rate_limit_seconds
