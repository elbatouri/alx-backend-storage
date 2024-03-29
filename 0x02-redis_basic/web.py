#!/usr/bin/env python3
""" expiring web cache module """

import redis
import requests
from typing import Callable
from functools import wraps

redis = redis.Redis()


def wrap_requests(fn: Callable) -> Callable:
    """ Decorator wrapper """

    @wraps(fn)
    def wrapper(url):
        """ Wrapper for decorator guy """
        redis.incr(f"count:{url}")
        cached_response = redis.get(f"cached:{url}")
        if cached_response:
            return cached_response.decode('utf-8')
        result = fn(url)
        redis.setex(f"cached:{url}", 10, result)
        return result

    return wrapper


@wrap_requests
def get_page(url: str) -> str:
    """get page self descriptive
    """
    response = requests.get(url)
    return response.text


if __name__ == "__main__":
    # Testing the implementation
    url = "http://google.com"
    print(get_page(url))  # This should fetch and cache the page from Google
    print(get_page(url))  # This should retrieve the cached page
    time.sleep(11)  # Let's wait for 11 seconds for the cache to expire
    print(get_page(url))  # This should fetch the page again as cache is expired
