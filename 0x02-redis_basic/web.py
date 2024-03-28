#!/usr/bin/env python3
'''A module for fetching web page content with caching and tracking.'''
import redis
import requests

redis_store = redis.Redis()


def data_cacher(method):
    '''Decorator to cache fetched data and track requests.'''
    def invoker(url):
        '''Wrapper function for caching fetched data.'''
        key_count = f'count:{url}'
        key_result = f'result:{url}'
        redis_store.incr(key_count)
        result = redis_store.get(key_result)
        if result:
            return result.decode('utf-8')
        result = method(url)
        redis_store.setex(key_result, 10, result)
        return result
    return invoker


@data_cacher
def get_page(url: str) -> str:
    '''Returns URL content, caching response and tracking request.'''
    return requests.get(url).text




if __name__ == "__main__":
    # Test the get_page function
    url = (
        "http://slowwly.robertomurray.co.uk/delay/1000/"
        "url/https://www.example.com"
    )
    print(get_page(url))
