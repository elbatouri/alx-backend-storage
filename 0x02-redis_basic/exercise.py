#!/usr/bin/env python3
'''using redis nosql storage'''
import uuid
import redis
from typing import Callable, Union


class Cache:
    '''Represents an object for storing data in a Redis data storage.
    '''
    def __init__(self) -> None:
        '''Initializes a Cache instance and connects to Redis.
        '''
        self._redis = redis.Redis()
        self._redis.flushdb()

    def store(self, data: Union[str, bytes, int, float]) -> str:
        '''Stores a value in Redis and returns the key.
        '''
        data_key = str(uuid.uuid4())
        self._redis.set(data_key, data)
        return data_key

    def get(self, key: str, fn: Callable = None) -> Union[str, bytes, None]:
        '''Retrieves a value from Redis and optionally applies a conversion function.
        '''
        value = self._redis.get(key)
        if value is not None and fn is not None:
            return fn(value)
        return value

    def get_str(self, key: str) -> str:
        '''Retrieves a string value from Redis.
        '''
        return self.get(key, fn=lambda x: x.decode('utf-8'))

    def get_int(self, key: str) -> int:
        '''Retrieves an integer value from Redis.
        '''
        return self.get(key, fn=lambda x: int(x))
