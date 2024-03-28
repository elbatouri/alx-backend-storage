#!/usr/bin/env python3
'''Module for request caching and tracking using Redis.'''
import redis
import requests
from functools import wraps
from typing import Callable

redis_store = redis.Redis()
'''Module-level Redis instance for caching and tracking.'''

def data_cacher(method: Callable) -> Callable:
    '''Decorator to cache fetched data and track requests.'''
    @wraps(method)
    def invoker(url) -> str:
        '''Wrapper function for caching fetched data.'''
        redis_store.incr(f'count:{url}')
        result = redis_store.get(f'result:{url}')
        if result:
            return result.decode('utf-8')
        result = method(url)
        redis_store.set(f'count:{url}', 0)
        redis_store.setex(f'result:{url}', 10, result)
        return result
    return invoker

@data_cacher
def get_page(url: str) -> str:
    '''Returns URL content, caching response and tracking request.'''
    return requests.get(url).text
