
# ai helped to make this cache module 
# use chatgpt 

from  cachetools import TTLCache
from threading import Lock
from typing import Any


cache = TTLCache(maxsize=1000, ttl=300)

cache_lock = Lock()


async def get_cache(key: str):
    with cache_lock:
        try:
            return cache[key]
        except:
            return None

async def set_cache(key: str, value: str):
    with cache_lock:
        cache[key] = value
async def delete_cache(key:str):
    with cache_lock:
        if key in cache:
            del cache[key]

async def clear_cache(key: str):
    with cache_lock:
        cache.clear()