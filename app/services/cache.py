
# ai helped to make this cache module 
# use chatgpt 

from  cachetools import TTLCache
from threading import RLock
from typing import Any


cache = TTLCache(maxsize=100, ttl=60)

cache_lock = RLock()


def get_cache(key: str):
    pass


def set_cache(key: str, value: str):
    pass