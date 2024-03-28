#!/usr/bin/env python3
'''using redis nosql storage'''
import uuid
import redis
from typing import Union


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

    def get(self, key: str) -> Union[str, bytes, None]:
        '''Retrieves a value from Redis.
        '''
        return self._redis.get(key)
