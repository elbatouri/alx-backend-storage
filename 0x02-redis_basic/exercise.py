#!/usr/bin/env python3
'''Using redis nosql storage'''

import uuid
import redis
from functools import wraps
from typing import Callable, Union


def count_calls(method: Callable) -> Callable:
    '''Decorator to count how many times methods of the Cache class are called.'''
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        '''Wrapper function that increments the count and calls the original method.'''
        # Increment count
        self._redis.incr(method.__qualname__)
        # Call the original method
        return method(self, *args, **kwargs)
    return wrapper


class Cache:
    '''Represents an object for storing data in a Redis data storage.'''
    def __init__(self) -> None:
        '''Initializes a Cache instance and connects to Redis.'''
        self._redis = redis.Redis()
        self._redis.flushdb()

    @count_calls
    def store(self, data: Union[str, bytes, int, float]) -> str:
        '''Stores a value in Redis and returns the key.'''
        data_key = str(uuid.uuid4())
        self._redis.set(data_key, data)
        return data_key

    def get(self, key: str) -> Union[str, bytes, None]:
        '''Retrieves a value from Redis.'''
        return self._redis.get(key)

    def get_str(self, key: str) -> str:
        '''Retrieves a string value from Redis.'''
        return self.get(key).decode('utf-8')

    def get_int(self, key: str) -> int:
        '''Retrieves an integer value from Redis.'''
        return int(self.get(key))
